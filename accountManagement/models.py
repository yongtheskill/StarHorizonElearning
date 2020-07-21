from django.db import models
from django.contrib.auth.models import AbstractUser
from StarHorizonElearning.storage_backends import MediaStorage

# Create your models here.

class Course(models.Model):
    
    courseName = models.CharField(max_length=200, verbose_name="course name")
    courseInstitution = models.CharField(max_length=200, verbose_name="institution", null=True)
    courseDescription = models.CharField(max_length=5000, verbose_name="course description", null=True, default=None)

    def __str__(self):
         return self.courseName


class StudentClass(models.Model):

    className = models.CharField(max_length=200, verbose_name="class name")
    classInstitution = models.CharField(max_length=200, verbose_name="institution", null=True)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return self.className

class Module(models.Model):

    moduleName = models.CharField(max_length=200, verbose_name="module name")
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.moduleName

class User(AbstractUser):

    institution = models.CharField(max_length=200, blank=True, null=True)
    phoneNumber = models.CharField(verbose_name="phone number", max_length=20, blank=True, null=True, default=None)
    profilePic = models.ImageField(storage=MediaStorage(), verbose_name="Profile picture", blank=True) 
    
    ACC_TYPES = [
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    ]
    accountType = models.CharField(verbose_name="account type", max_length=16, choices=ACC_TYPES, default="Administrator")
    classes = models.ManyToManyField(StudentClass, blank=True)

    quizResponses = models.CharField(max_length=1000000000, verbose_name="quizResponses", null=True)
    

    def __str__(self):
        return self.username