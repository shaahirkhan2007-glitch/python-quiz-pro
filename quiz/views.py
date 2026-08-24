from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .models import Question, Result

import random


# ==================================================
# HOME
# ==================================================

def home(request):
    return render(request, "home.html")


# ==================================================
# QUIZ
# ==================================================

@login_required
def quiz(request):

    # ----------------------------------------------
    # CREATE A NEW QUIZ SESSION
    # ----------------------------------------------

    if "questions" not in request.session:

        question_ids = list(
            Question.objects.values_list("id", flat=True)
        )

        # Need at least 10 questions
        if len(question_ids) < 10:
            return render(request, "quiz.html", {
                "message": "Please add at least 10 questions in Admin."
            })

        # Randomize all questions
        random.shuffle(question_ids)

        # USE EXACTLY 10 QUESTIONS
        request.session["questions"] = question_ids[:10]
        request.session["qno"] = 0
        request.session["score"] = 0

        request.session.modified = True

    # ----------------------------------------------
    # GET QUIZ SESSION
    # ----------------------------------------------

    question_ids = request.session.get("questions", [])
    qno = request.session.get("qno", 0)
    score = request.session.get("score", 0)

    # Safety check
    if not question_ids:
        request.session.pop("questions", None)
        request.session.pop("qno", None)
        request.session.pop("score", None)

        return redirect("quiz")

    # ----------------------------------------------
    # QUIZ FINISHED
    # ----------------------------------------------

    if qno >= len(question_ids):

        total = len(question_ids)

        Result.objects.create(
            user=request.user,
            score=score,
            total=total
        )

        # Clear quiz session
        request.session.pop("questions", None)
        request.session.pop("qno", None)
        request.session.pop("score", None)

        return render(request, "result.html", {
            "score": score,
            "total": total
        })

    # ----------------------------------------------
    # GET CURRENT QUESTION
    # ----------------------------------------------

    try:
        question = Question.objects.get(
            id=question_ids[qno]
        )

    except Question.DoesNotExist:

        # Remove invalid quiz session
        request.session.pop("questions", None)
        request.session.pop("qno", None)
        request.session.pop("score", None)

        return redirect("quiz")

    # ----------------------------------------------
    # SUBMIT ANSWER
    # ----------------------------------------------

    if request.method == "POST":

        selected_answer = request.POST.get("answer")

        # Check answer
        if selected_answer == question.answer:
            request.session["score"] = score + 1

        # Move to next question
        request.session["qno"] = qno + 1

        request.session.modified = True

        return redirect("quiz")

    # ----------------------------------------------
    # DISPLAY QUESTION
    # ----------------------------------------------

    return render(request, "quiz.html", {
        "question": question,
        "current": qno + 1,
        "total": len(question_ids),
    })


# ==================================================
# REGISTER
# ==================================================

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


# ==================================================
# LOGIN
# ==================================================

def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("/")

        return render(request, "login.html", {
            "error": "Invalid username or password.",
            "username": username
        })

    return render(request, "login.html")


# ==================================================
# LOGOUT
# ==================================================

def logout_user(request):

    logout(request)

    return redirect("/")


# ==================================================
# DASHBOARD
# ==================================================

@login_required
def dashboard(request):

    results = Result.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(request, "dashboard.html", {
        "results": results
    })


# ==================================================
# LEADERBOARD
# ==================================================

def leaderboard(request):

    results = Result.objects.order_by(
        "-score",
        "date"
    )[:10]

    return render(request, "leaderboard.html", {
        "results": results
    })