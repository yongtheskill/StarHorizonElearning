from django.db import models
from StarHorizonElearning.storage_backends import MediaStorage
from accountManagement.models import Module

# Create your models here.
class Video(models.Model):
    
    videoName = models.CharField(max_length=200, verbose_name="video name")
    videoID = models.CharField(max_length=200, verbose_name="video id")
    additionalComments = models.CharField(max_length=5000, verbose_name="additional comments", null=True) 
    videoFile = models.FileField(storage=MediaStorage()) 
    #the url to be linked for students to go to after watching the video
    afterAction = models.CharField(max_length=200, verbose_name="action to take after video")
    completeionURL = models.CharField(max_length=1000, verbose_name="url to go to after completion", null=True) 
    creationDate = models.DateTimeField(auto_now_add=True)

    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
         return self.videoName