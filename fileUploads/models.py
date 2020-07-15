from django.db import models
from StarHorizonElearning.storage_backends import MediaStorage

# Create your models here.
class FileUpload(models.Model):
    
    fileName = models.CharField(max_length=200, verbose_name="file name")
    filID = models.CharField(max_length=200, verbose_name="file id")
    uploadedFile = models.FileField(storage=MediaStorage()) 


    def __str__(self):
         return self.fileName