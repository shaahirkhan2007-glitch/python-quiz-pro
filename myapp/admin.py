from django.contrib import admin
from .models import Question, Result

admin.site.register(Question)
admin.site.register(Result)