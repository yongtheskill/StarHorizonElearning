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

        if not re.match(r"^[a-zA-Z0-9_]+$", lessonName):
            context = {"moduleObjects": Module.objects.all, "error": "No spaces or special characters are allowed in the lesson name"}
            return render(request, 'liveLesson/create.html', context)

        streamDate += streamTime
        streamDateTime = datetime.strptime(streamDate, "%b %d, %Y%I:%M %p")

        streamDuration = timedelta(minutes = float(streamDuration))

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


#livestream edit page
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

        streamDuration = timedelta(minutes = float(streamDuration))

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

        duration = lessonObj.streamDuration.total_seconds() / 60
        if duration % 1 == 0:
            duration = str(duration)[:-2]
        else:
            duration = str(duration)

        context = {"lesson": lessonObj, "startDate": startDate, "startTime": startTime, "duration": duration, "moduleObjects": Module.objects.all, }
        return render(request, 'liveLesson/edit.html', context)


#livestream creation page
@login_required
def joinLiveLesson(request, StreamID):
    
    username = urllib.parse.quote(request.user.username)

    if request.user.accountType == 'Teacher':
        """
        ec2 = boto3.resource('ec2', region_name="ap-southeast-1", aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        liveInstance = ec2.Instance(settings.LIVE_EC2_ID)
        if liveInstance.state['Name'] == 'running':
            isRunning = True
        else:
            isRunning = False

        if not isRunning:
            liveInstance.start()
            print("starting instance...")
        """
        startTime = LiveLesson.objects.get(lessonName = StreamID).streamTime
        ttl = startTime - sgt.localize(datetime.now())
        ttl = ttl.total_seconds() - 180

    
    else:
        startTime = LiveLesson.objects.get(lessonName = StreamID).streamTime
        ttl = startTime - sgt.localize(datetime.now())
        ttl = ttl.total_seconds()

        
    context = {"ttl": ttl, "StreamID": StreamID, "usr": username, }

    return render(request, 'liveLesson/join.html', context)


def cleanupLivestreamServer(request):
    
    ec2 = boto3.resource('ec2', region_name="ap-southeast-1", aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    liveInstance = ec2.Instance(settings.LIVE_EC2_ID)
    if liveInstance.state['Name'] == 'running':
        isRunning = True
    else:
        isRunning = False


    nowTime = sgt.localize(datetime.now())
    liveLessonObjects = LiveLesson.objects.all()
    shouldStop = True
    shouldStart = False

    for lessonObject in liveLessonObjects:
        #how many seconds in the future
        diffstTime = lessonObject.streamTime - nowTime
        diffendTime = lessonObject.streamEndTime - nowTime
        if diffendTime.total_seconds() > -300 and diffstTime.total_seconds() < 660:
            shouldStop = False
            if diffstTime.total_seconds() < 600:
                shouldStart = True
        if diffendTime.total_seconds() < -2880:
            lessonObject.delete()


    actionTaken = ""

    if shouldStop and isRunning:
        liveInstance.stop()
        actionTaken = " and is being stopped"

    if shouldStart and not isRunning:
        liveInstance.start()
        actionTaken = " and is being started"



    if isRunning:
        return HttpResponse("Server is Up" + actionTaken)
    else:
        return HttpResponse("Server is Down" + actionTaken)
    

#server status check api
def serverStatus(request):
    url = "https://live.gotutor.sg/#/"
    try:
        x = requests.get(url, timeout=4)
    except:
        return HttpResponse("Down")

    print(x.status_code)
    if x.status_code == 200:
        return HttpResponse("Up")
    else:
        return HttpResponse("Down")
    



#server status check api
def ongoingstream(request, StreamID):
    context = {"isHome": True}
    return render(request, 'home/home.html', context)