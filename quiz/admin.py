from django.contrib import admin
from .models import Question, Result


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "answer",
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "score",
        "total",
        "date",
    )