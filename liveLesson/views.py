from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from accountManagement.models import Module
from .models import LiveLesson

import requests
from datetime import datetime, timedelta
import pytz
import re
import urllib.parse

import boto3
from StarHorizonElearning import settings

sgt = pytz.timezone("Asia/Singapore")

#livestream management page
@login_required
def manageLiveLessons(request):

    context = {"lessonObjects": LiveLesson.objects.all, }

    return render(request, 'liveLesson/manage.html', context)


#livestream creation page
@login_required
def createLiveLesson(request):
    if request.user.accountType != 'Teacher':
        context = {"notAuthorised": True}
        return render(request, 'liveLesson/manage.html', context)

    #if submitting form
    if request.method == 'POST':
        lessonName = request.POST['lessonName']
        lessonDesc = request.POST['lessonDesc']
        streamID = lessonName
        streamDate = request.POST['streamDate']
        streamTime = request.POST['streamTime']
        streamDuration = request.POST['streamDuration']
        moduleID = request.POST['moduleID']

        if not re.match(r"^[a-zA-Z1-9]+$", lessonName):
            context = {"moduleObjects": Module.objects.all, "error": "No spaces or special characters are allowed in the lesson name"}
            return render(request, 'liveLesson/create.html', context)

        streamDate += streamTime
        streamDateTime = datetime.strptime(streamDate, "%b %d, %Y%I:%M %p")

        streamDuration = timedelta(hours = float(streamDuration))

        streamEndTime = streamDateTime + streamDuration
        print(type(streamDateTime))

        module = Module.objects.get(pk = moduleID)

        newLiveLesson = LiveLesson()
        newLiveLesson.lessonName = lessonName
        newLiveLesson.lessonDesc = lessonDesc
        newLiveLesson.streamID = streamID
        newLiveLesson.streamTime = sgt.localize(streamDateTime)
        newLiveLesson.streamDuration = streamDuration
        newLiveLesson.streamEndTime = sgt.localize(streamEndTime)
        newLiveLesson.module = module
        newLiveLesson.save()
        
        context = {"lessonObjects": LiveLesson.objects.all, "notification": "Successfully created live lesson"}
        return render(request, 'liveLesson/manage.html', context)


    else:
        context = {"moduleObjects": Module.objects.all, }
        return render(request, 'liveLesson/create.html', context)


#livestream creation page
@login_required
def editLiveLesson(request, StreamID):
    if request.user.accountType != 'Teacher':
        context = {"notAuthorised": True}
        return render(request, 'liveLesson/manage.html', context)
    
    #if submitting form
    if request.method == 'POST':
        lessonName = request.POST['lessonName']
        lessonDesc = request.POST['lessonDesc']
        streamID = lessonName
        streamDate = request.POST['streamDate']
        streamTime = request.POST['streamTime']
        streamDuration = request.POST['streamDuration']
        moduleID = request.POST['moduleID']

        streamDate += streamTime
        streamDateTime = datetime.strptime(streamDate, "%b %d, %Y%I:%M %p")

        streamDuration = timedelta(hours = float(streamDuration))

        streamEndTime = streamDateTime + streamDuration
        print(type(streamDateTime))

        module = Module.objects.get(pk = moduleID)

        newLiveLesson = LiveLesson.objects.get(lessonName = lessonName)
        newLiveLesson.lessonName = lessonName
        newLiveLesson.lessonDesc = lessonDesc
        newLiveLesson.streamID = streamID
        newLiveLesson.streamTime = sgt.localize(streamDateTime)
        newLiveLesson.streamDuration = streamDuration
        newLiveLesson.streamEndTime = sgt.localize(streamEndTime)
        newLiveLesson.module = module
        newLiveLesson.save()
        
        context = {"lessonObjects": LiveLesson.objects.all, "notification": "Successfully edited live lesson"}
        return render(request, 'liveLesson/manage.html', context)


    else:
        lessonObj = LiveLesson.objects.get(lessonName = StreamID)

        startDate = lessonObj.streamTime.strftime("%b %d, %Y")
        startTime = lessonObj.streamTime.strftime("%I:%M %p")

        duration = lessonObj.streamDuration.total_seconds() / 3600
        if duration % 1 == 0:
            duration = str(duration)[:-2]
        else:
            duration = str(duration)

        context = {"lesson": lessonObj, "startDate": startDate, "startTime": startTime, "duration": duration, "moduleObjects": Module.objects.all, }
        return render(request, 'liveLesson/edit.html', context)


#livestream creation page
@login_required
def joinLiveLesson(request, StreamID):
    
    if request.user.accountType == 'Teacher':
        
        ec2 = boto3.resource('ec2', region_name="ap-southeast-1", aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        liveInstance = ec2.Instance(settings.LIVE_EC2_ID)
        if liveInstance.state['Name'] == 'running':
            isRunning = True
        else:
            isRunning = False

        if not isRunning:
            liveInstance.start()
            print("starting instance...")

        username = urllib.parse.quote(request.user.username)

        context = {"ttl": 0, "StreamID": StreamID, "usr": username, "isTeacher": True, }
    
    else:
        startTime = LiveLesson.objects.get(lessonName = StreamID).streamTime
        ttl = startTime - sgt.localize(datetime.now())
        ttl = ttl.total_seconds()

        
        username = urllib.parse.quote(request.user.username)


        context = {"ttl": ttl, "StreamID": StreamID, "usr": username, }

    return render(request, 'liveLesson/join.html', context)


def cleanupLivestreamServer(request):
    
    ec2 = boto3.resource('ec2', region_name="ap-southeast-1", aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    liveInstance = ec2.Instance(settings.LIVE_EC2_ID)
    if liveInstance.state['Name'] == 'running':
        isRunning = True
    else:
        isRunning = False

    actionTaken = ""

    if isRunning == True:
        nowTime = sgt.localize(datetime.now())
        liveLessonObjects = LiveLesson.objects.all()
        shouldStop = True
        for lessonObject in liveLessonObjects:
            diffendTime = lessonObject.streamEndTime - nowTime
            diffstTime = lessonObject.streamTime - nowTime
            if diffendTime.total_seconds() > -1800 and diffstTime.total_seconds() < -1800:
                shouldStop = False
            if diffendTime.total_seconds() < -604800:
                lessonObject.delete()
        if shouldStop:
            liveInstance.stop()
            actionTaken = " and is being stopped"
        else:
            actionTaken = " and is not being stopped"


    url = "https://lv.shel.ml/#/"
    try:
        x = requests.get(url, timeout=4)
    except:
        return HttpResponse("Server is Down")

    print(x.status_code)
    if x.status_code == 200:
        return HttpResponse("Server is Up" + actionTaken)
    else:
        return HttpResponse("Server is Down")
    

#server status check api
def serverStatus(request):
    url = "https://lv.shel.ml/#/"
    try:
        x = requests.get(url, timeout=4)
    except:
        return HttpResponse("Down")

    print(x.status_code)
    if x.status_code == 200:
        return HttpResponse("Up")
    else:
        return HttpResponse("Down")