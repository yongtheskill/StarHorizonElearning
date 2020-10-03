from django.urls import path

from . import views

urlpatterns = [
    path('manage/', views.manageVideoLessons, name='manageVideoLessons'),
    path('view/<str:videoID>/', views.viewVideo, name='viewVideo'),
    path('deleteVideo/', views.deleteVideo, name='deleteVideo'),

]