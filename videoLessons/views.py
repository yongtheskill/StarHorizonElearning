from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Video


# Management page
def manageVideoLessons(request):

    return render(request, 'videoLessons/manage.html')
