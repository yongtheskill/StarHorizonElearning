from django.db import models

# Create your models here.
class Video(models.Model):
    
    videoName = models.CharField(max_length=200, verbose_name="video name")
    videoURL = models.CharField(max_length=1000, verbose_name="video url", null=True)
    completeionURL = models.CharField(max_length=1000, verbose_name="url to go to after completion", null=True, default=None)

    def __str__(self):
         return self.courseName