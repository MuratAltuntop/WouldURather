from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Choice


class QuestionCreateForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        label="İkilemin Nedir?",
        widget=forms.TextInput(
            attrs={
                "class": "neon-input",
                "placeholder": "Örn: Görünmez olmak mı, zamanı durdurabilmek mi?",
                "autocomplete": "off",
                "required": True,
            }
        ),
    )
    choice_a = forms.CharField(
        max_length=150,
        label="1. Taraf (A Seçeneği)",
        widget=forms.TextInput(
            attrs={
                "class": "neon-input neon-input-cyan",
                "placeholder": "Örn: Görünmez olmak 👻",
                "autocomplete": "off",
                "required": True,
            }
        ),
    )
    choice_b = forms.CharField(
        max_length=150,
        label="2. Taraf (B Seçeneği)",
        widget=forms.TextInput(
            attrs={
                "class": "neon-input neon-input-pink",
                "placeholder": "Örn: Zamanı durdurmak ⏳",
                "autocomplete": "off",
                "required": True,
            }
        ),
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        label="E-posta (İsteğe bağlı - Profilinizde ASLA görünmez)",
        widget=forms.EmailInput(
            attrs={
                "class": "neon-input",
                "placeholder": "ornek@email.com (Gizli tutulur)",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "neon-input",
            "placeholder": "Kullanıcı adınızı seçin",
            "autocomplete": "username",
        })
        self.fields["username"].help_text = ""
        if "password1" in self.fields:
            self.fields["password1"].widget.attrs.update({
                "class": "neon-input",
                "placeholder": "En az 8 karakter",
            })
            self.fields["password1"].help_text = ""
        if "password2" in self.fields:
            self.fields["password2"].widget.attrs.update({
                "class": "neon-input",
                "placeholder": "Şifrenizi tekrar girin",
            })
            self.fields["password2"].help_text = ""
