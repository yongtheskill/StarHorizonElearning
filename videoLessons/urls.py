from django.urls import path

from . import views

urlpatterns = [
    path('manage/', views.manageVideoLessons, name='manageVideoLessons'),

]