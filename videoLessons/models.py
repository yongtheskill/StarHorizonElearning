from django.db import models

# Create your models here.
class Video(models.Model):
    
    videoName = models.CharField(max_length=200, verbose_name="video name")
    videoID = models.CharField(max_length=200, verbose_name="video id")
    videoURL = models.CharField(max_length=1000, verbose_name="video url", null=True)
    #the url to be linked for students to go to after watching the video
    completeionURL = models.CharField(max_length=1000, verbose_name="url to go to after completion", null=True) 
    videoFile = models.FileField()

    def __str__(self):
         return self.courseName