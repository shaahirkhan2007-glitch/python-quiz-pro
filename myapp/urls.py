from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/', views.quiz, name='quiz'),
    #path('check/', views.check, name='check'),
   # path('result/', views.result, name='result'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),

]