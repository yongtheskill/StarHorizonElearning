from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    phoneNumber = models.CharField(verbose_name='phone number', max_length=20, blank=True, null=True, default=None)

    def __str__(self):
        return self.username