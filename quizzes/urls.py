from django.urls import path

from . import views

urlpatterns = [
    path('manage/', views.manageQuizzes, name='manageQuizzes'),
    path('create/', views.createQuiz, name='createQuizzes'),
    path('view/<str:quizID>/', views.viewQuiz, name='viewQuiz'),
    path('edit/<str:quizID>/', views.editQuiz, name='editQuiz'),
    path('do/<str:quizID>/', views.doQuiz, name='doQuiz'),
]