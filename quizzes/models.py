from django.db import models

from accountManagement.models import Course

# Create your models here.
class Quiz(models.Model):
    
    quizName = models.CharField(max_length=200, verbose_name="quiz name")
    quizID = models.CharField(max_length=200, verbose_name="quiz id")
    quizDueDate = models.DateTimeField(blank=True, null=True)

    quizData = models.CharField(max_length=10000000, verbose_name="quiz data")

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
         return self.quizName
