from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Quiz


import pytz
sgp = pytz.timezone('Asia/Singapore')
from datetime import datetime



#quiz management page
@login_required
def manageQuizzes(request):

    context = {"quizObjects": Quiz.objects.all, }

    return render(request, 'quizzes/manage.html', context)
    




#quiz creation page
@login_required
def createQuiz(request):
    nowTime = datetime.now()
    timestamp = nowTime.strftime("%Y-%m-%d-%H-%M")

    context = {"quizIDtoUse": "quiz%s" % (timestamp), }

    return render(request, 'quizzes/create.html', context)
