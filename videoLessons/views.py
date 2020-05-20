from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

import re

from .fileHandler import handle_uploaded_file

from .models import Video

import pytz
sgp = pytz.timezone('Asia/Singapore')
from datetime import datetime


#management page
@login_required
def manageVideoLessons(request):
    nowTime = datetime.now()
    timestamp = nowTime.strftime("%Y-%m-%d-%H-%M")

    baseContext = {"videoLessonObjects": Video.objects.all, "videoIDtoUse": "vid%s" % (timestamp)}

    if request.user.accountType != 'Teacher':
        context = {"notAuthorised": True}
        return render(request, 'videoLessons/manage.html', context)


    #if submitting project to be created
    if request.method == 'POST':

        #if video is being created
        if request.POST["managementAction"] == "create":
            #get values from submitted form
            videoName = request.POST["videoName"]
            additionalComments = request.POST["additionalComments"]
            videoID = request.POST["videoID"]


            #validate that video name is unique
            if (Video.objects.filter(videoName=videoName).exists()):
                context = {**baseContext, "error":"Sorry, a video with this name already exists, please choose a different name for your video.", }
                return render(request, 'videoLessons/manage.html', context)
            else:

                if 'videoFile' in request.FILES:
                    #check if mp4 file
                    if not re.findall(".*\.mp4$", request.POST["fileName"], flags=re.I):
                        #if not mp4
                        context = {**baseContext, "error":"Sorry, your video format was not recognised, please upload the video in .mp4 format.", }
                        return render(request, 'videoLessons/manage.html', context)

                    #handle files
                    request.FILES['videoFile'].name = "%s.mp4" % (videoID) 
                    if (Video.objects.filter(videoFile=request.FILES['videoFile']).exists()):
                        #return error
                        context = {**baseContext, "error": "Error, the video ID already exists, please try again", }
                        return render(request, 'videoLessons/manage.html', context)

                
                else:
                    #return error
                    context = {**baseContext, "error": "No video file uploaded, please select a video file to upload", }
                    return render(request, 'videoLessons/manage.html', context)


                #create project with entered values
                newVideo = Video()
                newVideo.videoName = videoName
                newVideo.additionalComments = additionalComments
                newVideo.videoID = videoID
                newVideo.videoFile = request.FILES['videoFile']
                newVideo.completeionURL = "nothing for now"
                newVideo.save()
                #return success
                context = {**baseContext, "notification": "Video: %s successfully created!" % (videoName), }
                return render(request, 'videoLessons/manage.html', context)   

        #if editing video
        if request.POST["managementAction"] == "edit":  
            print (request.POST)


    else:
        #return empty form
        context = {**baseContext,}
        return render(request, 'videoLessons/manage.html', context)


























#video view page
@login_required
def viewVideo(request, videoID):
    videoFilename = "vid%s.mp4" % (videoID)
    videoObject = Video.objects.filter(videoFile=videoFilename)

    print(videoObject[0])
    if (videoObject.exists()):
        context = {"videoObject": videoObject[0]}
        return render(request, 'videoLessons/view.html', context)
    else:
        context = {"error": "Sorry, this video does not exist", "onModalCloseRedirect": "/"}
        return render(request, 'videoLessons/view.html', context)