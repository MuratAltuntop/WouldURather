from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questions.models import Question, Choice, Vote


class Command(BaseCommand):
    help = "Başlangıç örnek ikilemlerini ve admin kullanıcısını oluşturur."

    def handle(self, *args, **options):
        # Admin kullanıcısını (murat) oluştur
        admin_user, created = User.objects.get_or_create(
            username="murat",
            defaults={"is_staff": True, "is_superuser": True}
        )
        admin_user.set_password("1903")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        self.stdout.write(self.style.SUCCESS("Admin kullanıcısı güncellendi: murat / 1903"))

        # Başlangıç ikilemleri
        seed_questions = [
            {
                "title": "Süper Güç Seçimi: Görünmez olmak mı, zamanı durdurabilmek mi?",
                "a": "Görünmez olmak 👻",
                "b": "Zamanı durdurmak ⏳",
                "votes_a": 42,
                "votes_b": 58,
            },
            {
                "title": "Hayat İkilemi: Sınırsız para ama hiç internet olmaması mı, sınırsız internet ama asgari ücretle yaşamak mı?",
                "a": "Sınırsız para & Sıfır internet 💰",
                "b": "Sınırsız teknoloji & Asgari ücret 📱",
                "votes_a": 65,
                "votes_b": 35,
            },
            {
                "title": "Zihin Yeteneği: Tüm dünya dillerini anında konuşmak mı, tüm hayvanlarla konuşabilmek mi?",
                "a": "Tüm dilleri akıcı konuşmak 🌍",
                "b": "Tüm hayvanlarla sohbet etmek 🐾",
                "votes_a": 51,
                "votes_b": 49,
            },
            {
                "title": "Zaman Yolculuğu: Geçmişe gidip büyük bir hatanı silmek mi, 10 yıl geleceğe gidip piyango sonucunu görmek mi?",
                "a": "Geçmişteki hatayı silmek ⏪",
                "b": "Geleceğin zengini olmak ⏩",
                "votes_a": 38,
                "votes_b": 62,
            },
            {
                "title": "Oyun Dünyası: En sevdiğin oyunun evreninde ana karakter olmak mı, istediğin her an gerçek dünyayı duraklatabilmek mi?",
                "a": "Oyun evreninde yaşamak 🎮",
                "b": "Gerçek dünyayı duraklatmak ⏸️",
                "votes_a": 44,
                "votes_b": 56,
            },
        ]

        for q_data in seed_questions:
            question, q_created = Question.objects.get_or_create(
                title=q_data["title"],
                defaults={"author": admin_user}
            )
            if q_created:
                Choice.objects.create(
                    question=question,
                    choice_text=q_data["a"],
                    votes=q_data["votes_a"],
                    order=1
                )
                Choice.objects.create(
                    question=question,
                    choice_text=q_data["b"],
                    votes=q_data["votes_b"],
                    order=2
                )
                self.stdout.write(self.style.SUCCESS(f"İkilem eklendi: {question.title}"))

        self.stdout.write(self.style.SUCCESS("Örnek veriler başarıyla Supabase'e yüklendi!"))
