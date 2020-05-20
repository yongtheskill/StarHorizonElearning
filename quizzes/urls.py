from django.urls import path

from . import views

urlpatterns = [
    path('manage/', views.manageQuizzes, name='manageQuizzes'),
    path('create/', views.createQuiz, name='createQuizzes'),
]