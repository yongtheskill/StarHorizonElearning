from django.db import models

from accountManagement.models import Module

import pytz
sgt = pytz.timezone('Asia/Singapore')

from datetime import datetime

# Create your models here.
class Quiz(models.Model):
    
    quizName = models.CharField(max_length=200, verbose_name="quiz name")
    quizID = models.CharField(max_length=200, verbose_name="quiz id")
    quizDueDate = models.DateTimeField(blank=True, null=True)
    creationDate = models.DateTimeField(auto_now_add=True)

    quizData = models.CharField(max_length=10000000, verbose_name="quiz data")

    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    repeatNumber = models.IntegerField(verbose_name="repeat number")

    class Meta:
        verbose_name_plural = "Quizzes"

    @property
    def isDue(self):
        return sgt.localize(datetime.now()) > self.quizDueDate

    def __str__(self):
         return self.quizName
