from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import FileUpload
from accountManagement.models import Course, User

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
def createFile(request):
    nowTime = datetime.now()
    timestamp = nowTime.strftime("%Y-%m-%d-%H-%M")

    context = {"quizIDtoUse": "quiz%s" % (timestamp), "courseObjects": Course.objects.all, }
    
    #if uploadig file
    if request.method == 'POST':

            #get values from submitted form
            fileName = request.POST["fileName"]
            fileID = request.POST["fileID"]

            #validate that video name is unique
            if (FileUpload.objects.filter(fileName=fileName).exists()):
                context = {**baseContext, "error":"Sorry, a file with this name already exists, please choose a different name for your file.", }
                return render(request, 'fileUploads/manage.html', context)
            else:

                if 'uploadedFile' in request.FILES:
                    #check if mp4 file
                    fileExtension = re.findall(r"\..*", request.POST["fileName"])[-1]

                    #handle files
                    request.FILES['videoFile'].name = "%s%s" % (videoID, fileExtension) 
                    if (Video.objects.filter(videoFile=request.FILES['videoFile']).exists()):
                        #return error
                        context = {**baseContext, "error": "Error, the video ID already exists, please try again", }
                        return render(request, 'videoLessons/manage.html', context)

                
                else:
                    #return error
                    context = {**baseContext, "error": "No video file uploaded, please select a video file to upload", }
                    return render(request, 'videoLessons/manage.html', context)


                #find matching course
                assignedCourseID = request.POST["assignedCourse"]
                assignedCourse = Course.objects.get(pk=assignedCourseID)

                #create project with entered values
                newVideo = Video()
                newVideo.videoName = videoName
                newVideo.additionalComments = additionalComments
                newVideo.videoID = videoID
                newVideo.videoFile = request.FILES['videoFile']
                newVideo.afterAction = afterAction
                newVideo.completeionURL = "nothing for now"
                newVideo.course = assignedCourse
                newVideo.save()
                #return success
                context = {**baseContext, "notification": "Video: %s successfully created!" % (videoName), }
                return render(request, 'videoLessons/manage.html', context)   


    else:
        return render(request, 'quizzes/create.html', context)



#quiz view page
@login_required
def downloadFile(request, fileID):

    context = {"fileObject": FileUpload.objects.get(fileID=fileID), }

    return render(request, 'fileUploads/view.html', context)


