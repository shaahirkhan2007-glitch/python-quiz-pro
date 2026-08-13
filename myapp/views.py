from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Question, Result
import random


# ---------------- HOME ----------------

def home(request):
    return render(request, "home.html")


# ---------------- QUIZ ----------------

@login_required
def quiz(request):

    # Get all question IDs
    all_ids = list(Question.objects.values_list("id", flat=True))

    if len(all_ids) == 0:
        return render(request, "quiz.html", {
            "message": "No questions found. Please add questions in Admin."
        })

    # Use only the first 10 random questions
    if "questions" not in request.session:

        random.shuffle(all_ids)

        request.session["questions"] = all_ids[:10]
        request.session["qno"] = 0
        request.session["score"] = 0

    question_ids = request.session["questions"]
    qno = request.session["qno"]

    # Finish quiz
    if qno >= len(question_ids):

        score = request.session["score"]

        if request.user.is_authenticated:
            Result.objects.create(
                user=request.user,
                score=score,
                total=len(question_ids)
            )

        request.session.pop("questions", None)
        request.session.pop("qno", None)
        request.session.pop("score", None)

        return render(request, "result.html", {
            "score": score,
            "total": len(question_ids)
        })

    try:
        question = Question.objects.get(id=question_ids[qno])
    except Question.DoesNotExist:

        request.session.pop("questions", None)
        request.session.pop("qno", None)
        request.session.pop("score", None)

        return redirect("quiz")

    if request.method == "POST":

        selected = request.POST.get("answer")

        if selected == question.answer:
            request.session["score"] += 1

        request.session["qno"] += 1

        return redirect("quiz")

    return render(request, "quiz.html", {
        "question": question,
        "current": qno + 1,
        "total": len(question_ids)
    })


# ---------------- REGISTER ----------------

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")

    else:
        form = RegisterForm()

    return render(request, "register.html", {
        "form": form
    })


# ---------------- LOGIN ----------------

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
            return redirect("/")

        return render(request, "login.html", {
            "error": "Invalid Username or Password"
        })

    return render(request, "login.html")


# ---------------- LOGOUT ----------------

def logout_user(request):
    logout(request)
    return redirect("/")


# ---------------- DASHBOARD ----------------

@login_required
def dashboard(request):

    results = Result.objects.filter(user=request.user).order_by("-date")

    return render(request, "dashboard.html", {
        "results": results
    })


# ---------------- LEADERBOARD ----------------

def leaderboard(request):

    results = Result.objects.order_by("-score", "date")[:10]

    return render(request, "leaderboard.html", {
        "results": results
    })