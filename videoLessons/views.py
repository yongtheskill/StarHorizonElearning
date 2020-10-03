from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

import re

from .models import Video
from accountManagement.models import Module, Course

import pytz
sgp = pytz.timezone('Asia/Singapore')
from datetime import datetime


#management page
@login_required
def manageVideoLessons(request):
    nowTime = datetime.now()
    timestamp = nowTime.strftime("%Y-%m-%d-%H-%M")

    courseObjects = list(Course.objects.all())
    courseIDs = [i.id for i in courseObjects]

    baseContext = {"videoLessonObjects": Video.objects.all, "videoIDtoUse": "vid%s" % (timestamp), "courseObjects": courseObjects, "courseIDs": courseIDs ,"moduleObjects": Module.objects.all, }

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


                #find matching mod
                try:
                    assignedModID = request.POST["assignedMod"]
                    assignedMod = Module.objects.get(pk=assignedModID)
                except:                    
                    context = {**baseContext, "error":"Please provide a module.", }
                    return render(request, 'videoLessons/manage.html', context)

                #create project with entered values
                newVideo = Video()
                newVideo.videoName = videoName
                newVideo.additionalComments = additionalComments
                newVideo.videoID = videoID
                newVideo.videoFile = request.FILES['videoFile']
                newVideo.completeionURL = "nothing for now"
                newVideo.module = assignedMod
                newVideo.save()
                #return success
                context = {**baseContext, "notification": "Video: %s successfully created!" % (videoName), }
                return render(request, 'videoLessons/manage.html', context)   

        #if editing video
        if request.POST["managementAction"] == "edit":  
            #get values from submitted form
            additionalComments = request.POST["additionalComments"]
            videoID = request.POST["videoIDToEdit"]

            #validate that video name is unique
            if (Video.objects.filter(videoID=videoID).exists()):

                #create project with entered values
                newVideo = Video.objects.get(videoID=videoID)

                newVideo.additionalComments = additionalComments
                newVideo.save()
                #return success
                context = {**baseContext, "notification": "Video: %s successfully edited!" % (newVideo.videoName), }
                return render(request, 'videoLessons/manage.html', context)   


    else:
        #return empty form
        context = {**baseContext,}
        return render(request, 'videoLessons/manage.html', context)


def deleteVideo(request):
    nowTime = datetime.now()
    timestamp = nowTime.strftime("%Y-%m-%d-%H-%M")
    
    courseObjects = list(Course.objects.all())
    courseIDs = [i.id for i in courseObjects]

    if request.method == 'POST':
        
        videoID = request.POST['videoID']
        video = Video.objects.get(videoID = videoID)

        video.delete()


        context = {"videoLessonObjects": Video.objects.all, "videoIDtoUse": "vid%s" % (timestamp), "courseObjects": courseObjects, "courseIDs": courseIDs ,"moduleObjects": Module.objects.all, "notification": "Deleted video", }

        return render(request, 'videoLessons/manage.html', context)

    else:
        context = {"videoLessonObjects": Video.objects.all, "videoIDtoUse": "vid%s" % (timestamp), "courseObjects": courseObjects, "courseIDs": courseIDs ,"moduleObjects": Module.objects.all, "error": "unable to delete video", }

        return render(request, 'videoLessons/manage.html', context)


























#video view page
@login_required
def viewVideo(request, videoID):
    try:
        videoObject = Video.objects.get(videoID=videoID)
        context = {"videoObject": videoObject}
        return render(request, 'videoLessons/view.html', context)
    except: 
        context = {"error": "Sorry, this video does not exist", "onModalCloseRedirect": "/"}
        return render(request, 'videoLessons/view.html', context)