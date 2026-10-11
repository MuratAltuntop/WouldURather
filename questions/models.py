from django.db import models
from django.contrib.auth.models import User
from django.db.models import F


class Question(models.Model):
    """
    Kullanıcıların veya adminlerin oluşturduğu 'Hangisini Seçersin?' ikilemleri.
    """
    title = models.CharField(max_length=255, verbose_name="İkilem Başlığı")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Yazar"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "İkilem"
        verbose_name_plural = "İkilemler"

    def __str__(self):
        return self.title

    @property
    def choice_a(self):
        choices = self.choices.order_by("order", "id")
        return choices.first() if choices.exists() else None

    @property
    def choice_b(self):
        choices = self.choices.order_by("order", "id")
        return choices[1] if choices.count() > 1 else None

    @property
    def total_votes(self):
        a = self.choice_a
        b = self.choice_b
        return (a.votes if a else 0) + (b.votes if b else 0)

    @property
    def pct_a(self):
        total = self.total_votes
        if total == 0:
            return 50
        a = self.choice_a
        return round(((a.votes if a else 0) / total) * 100)

    @property
    def pct_b(self):
        total = self.total_votes
        if total == 0:
            return 50
        return 100 - self.pct_a

    def recent_voters(self):
        """
        Oy veren son kayıtlı kullanıcıların SADECE kullanıcı adlarını döner (E-posta kesinlikle dönmez).
        """
        return (
            self.votes_cast
            .filter(user__isnull=False)
            .select_related("user")
            .order_by("-created_at")[:6]
        )


class Choice(models.Model):
    """
    Her ikileme ait 2 seçenek (A ve B seçeneği).
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name="İkilem"
    )
    choice_text = models.CharField(max_length=150, verbose_name="Seçenek Metni")
    votes = models.PositiveIntegerField(default=0, verbose_name="Oy Sayısı")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Sıra (1: A, 2: B)")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Seçenek"
        verbose_name_plural = "Seçenekler"

    def __str__(self):
        return f"{self.question.title} - {self.choice_text}"


class Vote(models.Model):
    """
    Kullanıcıların veya anonim oturumların verdikleri oyların kaydı.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="votes_cast",
        verbose_name="İkilem"
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name="votes_cast",
        verbose_name="Seçilen Taraf"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="votes_cast",
        verbose_name="Kullanıcı (Üye ise)"
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Anonim Oturum Anahtarı"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oy Zamanı")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Oy Kaydı"
        verbose_name_plural = "Oy Kayıtları"
        constraints = [
            models.UniqueConstraint(
                fields=["question", "user"],
                condition=models.Q(user__isnull=False),
                name="unique_user_vote_per_question"
            )
        ]

    def __str__(self):
        user_display = self.user.username if self.user else f"Misafir ({self.session_key[:8] if self.session_key else 'Anonim'})"
        return f"{user_display} -> {self.choice.choice_text}"
