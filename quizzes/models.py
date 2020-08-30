from django.db import models

from accountManagement.models import Module

# Create your models here.
class Quiz(models.Model):
    
    quizName = models.CharField(max_length=200, verbose_name="quiz name")
    quizID = models.CharField(max_length=200, verbose_name="quiz id")
    quizDueDate = models.DateTimeField(blank=True, null=True)
    creationDate = models.DateTimeField(auto_now_add=True)

    quizData = models.CharField(max_length=10000000, verbose_name="quiz data")

    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
         return self.quizName
