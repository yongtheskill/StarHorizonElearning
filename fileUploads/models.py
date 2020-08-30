from django.db import models
from StarHorizonElearning.storage_backends import MediaStorage
from accountManagement.models import Module

# Create your models here.
class FileUpload(models.Model):
    
    fileName = models.CharField(max_length=200, verbose_name="file name")
    fileID = models.CharField(max_length=200, verbose_name="file id")
    uploadedFile = models.FileField(storage=MediaStorage()) 
    creationDate = models.DateTimeField(auto_now_add=True)

    module = models.ForeignKey(Module, on_delete=models.CASCADE)


    def __str__(self):
         return self.fileName