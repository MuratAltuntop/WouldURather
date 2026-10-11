import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import F
from django.core.paginator import Paginator

from .models import Question, Choice, Vote
from .forms import QuestionCreateForm, RegisterForm


def _get_voted_choice_ids(request, question_ids):
    """
    Kullanıcının veya misafir oturumunun verilen soru listesindeki oy tercihlerini
    {question_id: choice_id} sözlüğü olarak döner.
    """
    voted_map = {}
    if request.user.is_authenticated:
        votes = Vote.objects.filter(question_id__in=question_ids, user=request.user)
    else:
        if not request.session.session_key:
            request.session.save()
        votes = Vote.objects.filter(question_id__in=question_ids, session_key=request.session.session_key)
    
    for v in votes:
        voted_map[v.question_id] = v.choice_id
    return voted_map


def focus_view(request):
    """
    Ana Sayfa: Odak Modu (Tekil İkilem Kartı).
    Kullanıcıya tek bir ikilem kartı sunar, oylama sonrası animasyonla yüzdeler açılır
    ve 'Sıradaki İkilem' butonu görünür.
    """
    qid = request.GET.get("qid")
    question = None

    if qid:
        question = Question.objects.filter(id=qid, is_active=True).first()

    if not question:
        # Kullanıcının henüz oy vermediği bir soruyu bulmaya çalış
        if request.user.is_authenticated:
            voted_qids = Vote.objects.filter(user=request.user).values_list("question_id", flat=True)
        else:
            if not request.session.session_key:
                request.session.save()
            voted_qids = Vote.objects.filter(session_key=request.session.session_key).values_list("question_id", flat=True)

        unvoted = Question.objects.filter(is_active=True).exclude(id__in=voted_qids).order_by("?").first()
        question = unvoted if unvoted else Question.objects.filter(is_active=True).order_by("-created_at").first()

    voted_choice_id = None
    if question:
        voted_map = _get_voted_choice_ids(request, [question.id])
        voted_choice_id = voted_map.get(question.id)

    total_count = Question.objects.filter(is_active=True).count()

    context = {
        "question": question,
        "voted_choice_id": voted_choice_id,
        "total_questions_count": total_count,
        "active_nav": "focus",
    }
    return render(request, "questions/focus.html", context)


def next_question_view(request, current_id=None):
    """
    Odak modunda 'Sıradaki İkilem' butonuna tıklandığında henüz oy verilmemiş bir sonraki soruyu bulur.
    """
    if request.user.is_authenticated:
        voted_qids = set(Vote.objects.filter(user=request.user).values_list("question_id", flat=True))
    else:
        if not request.session.session_key:
            request.session.save()
        voted_qids = set(Vote.objects.filter(session_key=request.session.session_key).values_list("question_id", flat=True))

    qs = Question.objects.filter(is_active=True)
    if current_id:
        voted_qids.add(current_id)

    unvoted = qs.exclude(id__in=voted_qids).order_by("?").first()
    if not unvoted:
        # Tüm sorular oylandıysa farklı bir rastgele soruya yönlendir
        unvoted = qs.exclude(id=current_id).order_by("?").first() if current_id else qs.first()

    if unvoted:
        return redirect(f"/?qid={unvoted.id}")
    return redirect("home")


def feed_view(request):
    """
    Tüm İkilemler Akışı (Liste Modu).
    Tüm ikilemleri alt alta kartlar halinde listeler.
    """
    questions_qs = Question.objects.filter(is_active=True).select_related("author").prefetch_related("choices", "votes_cast__user")
    paginator = Paginator(questions_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    page_qids = [q.id for q in page_obj]
    voted_map = _get_voted_choice_ids(request, page_qids)

    context = {
        "page_obj": page_obj,
        "voted_map": voted_map,
        "active_nav": "feed",
    }
    return render(request, "questions/feed.html", context)


def vote_view(request, choice_id):
    """
    Asenkron (Fetch API) Oy Verme Endpoint'i.
    POST isteği ile çalışır.
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Geçersiz istek metodu."}, status=405)

    choice = get_object_or_404(Choice.objects.select_related("question"), id=choice_id)
    question = choice.question

    if not question.is_active:
        return JsonResponse({"success": False, "error": "Bu ikilem artık aktif değil."}, status=400)

    # Oturum veya kullanıcı kontrolü
    user = request.user if request.user.is_authenticated else None
    session_key = None
    if not user:
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key

    # Mükerrer oy kontrolü
    if user:
        existing_vote = Vote.objects.filter(question=question, user=user).first()
    else:
        existing_vote = Vote.objects.filter(question=question, session_key=session_key).first()

    if existing_vote:
        # Zaten oy verilmişse güncel oranları dön
        question.refresh_from_db()
        return JsonResponse({
            "success": True,
            "already_voted": True,
            "chosen_id": existing_vote.choice_id,
            "pct_a": question.pct_a,
            "pct_b": question.pct_b,
            "votes_a": question.choice_a.votes if question.choice_a else 0,
            "votes_b": question.choice_b.votes if question.choice_b else 0,
            "total_votes": question.total_votes,
            "message": "Bu ikileme daha önce oy verdiniz!",
        })

    # Yeni oyu kaydet
    Vote.objects.create(
        question=question,
        choice=choice,
        user=user,
        session_key=session_key,
    )

    # Oy sayısını atomik olarak artır
    Choice.objects.filter(id=choice.id).update(votes=F("votes") + 1)

    # Güncel durumu yeniden yükle
    question.refresh_from_db()

    # Son oy veren kullanıcıların SADECE kullanıcı adları (E-posta kesinlikle yok)
    voters = [v.user.username for v in question.recent_voters() if v.user]

    return JsonResponse({
        "success": True,
        "already_voted": False,
        "chosen_id": choice.id,
        "pct_a": question.pct_a,
        "pct_b": question.pct_b,
        "votes_a": question.choice_a.votes if question.choice_a else 0,
        "votes_b": question.choice_b.votes if question.choice_b else 0,
        "total_votes": question.total_votes,
        "recent_voters": voters,
    })


@login_required(login_url="login")
def create_question_view(request):
    """
    Yeni İkilem Yaratma Sayfası (Giriş zorunlu).
    """
    if request.method == "POST":
        form = QuestionCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].strip()
            choice_a_text = form.cleaned_data["choice_a"].strip()
            choice_b_text = form.cleaned_data["choice_b"].strip()

            question = Question.objects.create(
                title=title,
                author=request.user,
            )

            Choice.objects.create(
                question=question,
                choice_text=choice_a_text,
                order=1,
            )

            Choice.objects.create(
                question=question,
                choice_text=choice_b_text,
                order=2,
            )

            messages.success(request, "İkilemin başarıyla yayınlandı! Bakalım topluluk ne seçecek?")
            return redirect(f"/?qid={question.id}")
    else:
        form = QuestionCreateForm()

    return render(request, "questions/create.html", {"form": form, "active_nav": "create"})


@login_required(login_url="login")
def profile_view(request, username=None):
    """
    Kullanıcı Profil Sayfası:
    - Kullanıcının kendi sorduğu ikilemler (silme yetkisiyle)
    - Kullanıcının oy verdiği ikilemler ve tercihleri
    - GİZLİLİK: E-posta adresi hiçbir yerde gösterilmez!
    """
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user

    is_owner = (request.user == profile_user)

    user_questions = Question.objects.filter(author=profile_user).prefetch_related("choices")
    user_votes = (
        Vote.objects.filter(user=profile_user)
        .select_related("question", "choice")
        .order_by("-created_at")
    )

    context = {
        "profile_user": profile_user,
        "is_owner": is_owner,
        "user_questions": user_questions,
        "user_votes": user_votes,
        "active_nav": "profile" if is_owner else "",
    }
    return render(request, "auth/profile.html", context)


@login_required(login_url="login")
def delete_question_view(request, question_id):
    """
    Kullanıcının kendi sorusunu silmesi.
    """
    if request.method == "POST":
        question = get_object_or_404(Question, id=question_id, author=request.user)
        question.delete()
        messages.success(request, "İkilem başarıyla silindi.")
    return redirect("profile")


# ===================== AUTHENTICATION VIEWS =====================

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Hoş geldin @{user.username}! Artık kendi ikilemlerini sorabilirsin.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Tekrar hoş geldin @{user.username}!")
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Oturumun kapatıldı. Tekrar görüşmek üzere!")
    return redirect("home")
