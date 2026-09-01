from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Question, Result


def home(request):
    return render(request, "home.html")


@login_required
def quiz(request):

    questions = Question.objects.all()

    if request.method == "POST":

        score = 0
        total = questions.count()

        for question in questions:

            selected_answer = request.POST.get(
                f"question_{question.id}"
            )

            if selected_answer == question.answer:
                score += 1

        Result.objects.create(
            user=request.user,
            score=score,
            total=total
        )

        return render(
            request,
            "result.html",
            {
                "score": score,
                "total": total
            }
        )

    return render(
        request,
        "quiz.html",
        {
            "questions": questions
        }
    )


def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect("login")

    return render(request, "register.html")


def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "login.html")


def logout_user(request):

    logout(request)

    return redirect("home")


@login_required
def dashboard(request):

    results = Result.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(
        request,
        "dashboard.html",
        {
            "results": results
        }
    )


def leaderboard(request):

    results = Result.objects.select_related(
        "user"
    ).order_by(
        "-score",
        "date"
    )[:20]

    return render(
        request,
        "leaderboard.html",
        {
            "results": results
        }
    )