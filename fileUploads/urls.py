from django.urls import path

from . import views

urlpatterns = [
    path('manage/', views.manageUploads, name='manageUploadds'),
    path('upload/', views.uploadFile, name='uploadFile'),
    path('download/<str:fileID>', views.downloadFile, name='downloadFile'),
]