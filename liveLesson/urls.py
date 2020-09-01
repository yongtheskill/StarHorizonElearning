from django.urls import path

from . import views

urlpatterns = [
    path('', views.manageLiveLessons, name='manageLiveLessons'),
    path('create/', views.createLiveLesson, name='createLiveLessons'),
    path('edit/<str:StreamID>', views.editLiveLesson, name='editLiveLessons'),
    path('join/<str:StreamID>', views.joinLiveLesson, name='joinLiveLesson'),
    path('serverStatus/', views.serverStatus, name='serverStatus'),
    path('cleanupLivestreamServer/', views.cleanupLivestreamServer, name='cleanupLivestreamServer'),
    path('deleteStream/', views.deleteLiveLesson, name='deleteLiveLesson'),
    path('ongoingstream/<str:StreamID>/', views.ongoingstream, name='ongoingstream'),
    path('extend/<str:StreamID>/', views.extendStream, name='extendStream'),
    path('exitStream/', views.exitStream, name='exitStream'),
    

]