from django.urls import path

from . import views

urlpatterns = [
    path('manage/', views.manageUploads, name='manageUploadds'),
    path('upload/', views.uploadFile, name='uploadFile'),
    path('delete/<str:fileID>', views.deleteFile, name='deleteFile'),
]