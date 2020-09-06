from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import FileUpload
from accountManagement.models import Module, Course, User

import json
import re

import pytz
sgp = pytz.timezone('Asia/Singapore')
from datetime import datetime



#file management page
@login_required
def manageUploads(request):

    context = {"fileObjects": FileUpload.objects.all, }

    return render(request, 'fileUploads/manage.html', context)
    




#file creation page
@login_required
def uploadFile(request):
    nowTime = datetime.now()
    timestamp = nowTime.strftime("%Y-%m-%d-%H-%M")

    courseObjects = list(Course.objects.all())
    courseIDs = [i.id for i in courseObjects]

    baseContext = {"fileIDtoUse": "file%s" % (timestamp), "courseObjects": courseObjects, "courseIDs": courseIDs ,"moduleObjects": Module.objects.all, }
    
    #if uploadig file
    if request.method == 'POST':

            #get values from submitted form
            fileName = request.POST["fileName"]
            fileID = request.POST["fileID"]

            #validate that file name is unique
            if (FileUpload.objects.filter(fileName=fileName).exists()):
                context = {**baseContext, "error":"Sorry, a file with this name already exists, please choose a different name for your file.", }
                return render(request, 'fileUploads/manage.html', context)
            else:

                if 'uploadedFile' in request.FILES:
                    #get extension
                    fileExtension = re.findall(r"\..*", request.POST["fileName"])[-1]

                    #handle files
                    request.FILES['uploadedFile'].name = "%s%s" % (fileID, fileExtension) 
                    if (FileUpload.objects.filter(uploadedFile=request.FILES['uploadedFile']).exists()):
                        #return error
                        context = {**baseContext, "error": "Error, the file ID already exists, please try again", }
                        return render(request, 'fileUploads/manage.html', context)

                
                else:
                    #return error
                    context = {**baseContext, "error": "No file uploaded, please select a file to upload", }
                    return render(request, 'videoLessons/manage.html', context)


                #find matching course
                moduleID = request.POST["moduleID"]
                module = Module.objects.get(pk=moduleID)

                #create project with entered values
                newFile = FileUpload()
                newFile.fileName = fileName
                newFile.fileID = fileID
                newFile.uploadedFile = request.FILES['uploadedFile']
                newFile.module = module
                newFile.save()
                #return success
                context = {"fileObjects": FileUpload.objects.all, "notification": "File: %s successfully uploaded!" % (fileName), }
                return render(request, 'fileUploads/manage.html', context)   


    else:
        return render(request, 'fileUploads/create.html', baseContext)



#file edit page
@login_required
def deleteFile(request, fileID):
    
    #if editing file
    if request.method == 'POST':
        fileToDelete = FileUpload.objects.get(fileID=fileID)
        fileToDelete.uploadedFile.delete()
        fileToDelete.delete()

        context = {"fileObjects": FileUpload.objects.all, "notification": "File successfully deleted!", }
        return render(request, 'fileUploads/manage.html', context)



    else:
        fileToDelete = FileUpload.objects.get(fileID=fileID)
        context = {"fileToDelete": fileToDelete }
        return render(request, 'fileUploads/delete.html', context)


