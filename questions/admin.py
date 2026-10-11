from django.contrib import admin
from .models import Question, Choice, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    max_num = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "total_votes", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "author__username")
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "order", "votes")
    list_filter = ("order",)
    search_fields = ("choice_text", "question__title")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("question", "choice", "user", "session_key", "created_at")
    list_filter = ("created_at",)
    search_fields = ("question__title", "choice__choice_text", "user__username")
