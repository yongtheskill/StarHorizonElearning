from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


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
            completeionURL = request.POST["completeionURL"]


            #validate that video name is unique
            if (Video.objects.filter(videoName=videoName).exists()):
                #return values that were already filled so that they dont have to be entered again
                context = {"videoIDtoUse": timestamp, "error":"Sorry, a video with this name already exists, please choose a different name for your video.", }
                return render(request, 'videoLessons/manage.html', context)
            else:

                if 'videoFile' in request.FILES:
                    #handle files
                    fileStatus = handle_uploaded_file(request.FILES['videoFile'], videoID)
                    if fileStatus == "error":
                        #return error
                        context = {"videoIDtoUse": timestamp, "error": "Error, the video ID already exists, please try again", }
                        return render(request, 'videoLessons/manage.html', context)

                    else:
                        #set videoURL
                        videoURL = fileStatus
                
                else:
                    #return error
                    context = {"videoIDtoUse": timestamp, "error": "No video file uploaded, please select a video file to upload", }
                    return render(request, 'videoLessons/manage.html', context)


                #create project with entered values
                newVideo = Video()
                newVideo.videoName = videoName
                newVideo.additionalComments = additionalComments
                newVideo.videoID = videoID
                newVideo.videoURL = videoURL
                newVideo.completeionURL = completeionURL
                newVideo.save()
                #return success
                context = {"videoIDtoUse": timestamp, "notification": "Video: %s successfully created!" % (videoName), }
                return render(request, 'videoLessons/manage.html', context)   


        else:
            #return empty form
            context = {"videoIDtoUse": timestamp, }
            return render(request, 'videoLessons/manage.html', context)

    else:
        #return empty form
        context = {"videoIDtoUse": timestamp, }
        return render(request, 'videoLessons/manage.html', context)

