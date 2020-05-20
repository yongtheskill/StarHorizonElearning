from django.db import models

# Create your models here.
class Quiz(models.Model):
    
    quizName = models.CharField(max_length=200, verbose_name="quiz name")
    quizID = models.CharField(max_length=200, verbose_name="quiz ID")

    quizData = models.CharField(max_length=100000, verbose_name="quiz ID")

    def __str__(self):
         return self.quizName
