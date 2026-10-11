from django.urls import path
from . import views

urlpatterns = [
    # Ana Sayfa: Odak Modu
    path("", views.focus_view, name="home"),
    path("next/", views.next_question_view, name="next_question"),
    path("next/<int:current_id>/", views.next_question_view, name="next_question_from"),

    # Feed: Tüm İkilemler Listesi
    path("feed/", views.feed_view, name="feed"),

    # Asenkron Oy Verme API
    path("vote/<int:choice_id>/", views.vote_view, name="vote"),

    # Yeni İkilem Yarat (Login required)
    path("create/", views.create_question_view, name="create_question"),

    # Profil & Soru Silme
    path("profile/", views.profile_view, name="profile"),
    path("user/<str:username>/", views.profile_view, name="user_profile"),
    path("delete/<int:question_id>/", views.delete_question_view, name="delete_question"),

    # Kimlik Doğrulama
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
