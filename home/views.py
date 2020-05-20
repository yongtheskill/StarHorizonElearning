from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import datetime
import pytz
from django.utils import timezone


#home page
def home(request):
    context = {"isHome": True}
    return render(request, 'home/home.html', context)