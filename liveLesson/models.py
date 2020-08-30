from django.db import models
from accountManagement.models import Module

# Create your models here.
class LiveLesson(models.Model):
    
    lessonName = models.CharField(max_length=200, verbose_name="lesson name")
    lessonDesc = models.CharField(max_length=500, verbose_name="lesson description")
    streamID = models.CharField(max_length=200, verbose_name="stream id")
    streamTime = models.DateTimeField()
    streamDuration = models.DurationField()
    streamEndTime = models.DateTimeField()
    creationDate = models.DateTimeField(auto_now_add=True)

    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
         return self.lessonName