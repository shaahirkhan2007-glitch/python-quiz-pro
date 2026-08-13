from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question = models.CharField(max_length=500)

    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    score = models.IntegerField()

    total = models.IntegerField()

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total}"