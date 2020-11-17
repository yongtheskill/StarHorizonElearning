from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from accountManagement.models import User

import datetime
import pytz
from django.utils import timezone


#home page
def home(request):
    context = {"isHome": True}
    return render(request, 'home/home.html', context)


#timer
def addTime(request, username):
    try:
        userObject = User.objects.get(username = username)

        if not userObject.timeOnline:
            userObject.timeOnline = datetime.timedelta(seconds=0)

        userObject.timeOnline += datetime.timedelta(seconds=10)
        userObject.save()
    except:
        return HttpResponse("Not Available")

    return HttpResponse("Done")


def whiteboard(request):
    return render(request, 'home/whiteboard.html', {})


#data demo
def dataDemo(request):
    return render(request, 'home/dataDemo.html', {})