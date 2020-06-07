from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Quiz
from accountManagement.models import Course

import json
import re

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

    context = {"quizIDtoUse": "quiz%s" % (timestamp), "courseObjects": Course.objects.all, }
    
    #if submitting form
    if request.method == 'POST':
        questionsJSON = request.POST['allQuestionsJSON']
        questionsJSON = re.sub("_____var__", "", questionsJSON) #remove js stuff

        #find matching course
        assignedCourseID = request.POST["assignedCourse"]
        assignedCourse = Course.objects.get(pk=assignedCourseID)

        newQuiz = Quiz()
        newQuiz.quizName = request.POST['quizName']
        newQuiz.quizID = request.POST['quizID']
        newQuiz.course = assignedCourse
        newQuiz.quizData = questionsJSON
        newQuiz.save()
        
        context = {"quizObjects": Quiz.objects.all, "notification": "Successfully created quiz"}
        return render(request, 'quizzes/manage.html', context)


    else:
        return render(request, 'quizzes/create.html', context)



#quiz view page
@login_required
def viewQuiz(request, quizID):

    context = {"quizObject": Quiz.objects.get(quizID=quizID), }

    return render(request, 'quizzes/view.html', context)
    




#quiz edit page
@login_required
def editQuiz(request, quizID):
    
    #if submitting form
    if request.method == 'POST':
        questionsJSON = request.POST['allQuestionsJSON']
        questionsJSON = re.sub("_____var__", "", questionsJSON) #remove js stuff

        #find matching course
        assignedCourseID = request.POST["assignedCourse"]
        assignedCourse = Course.objects.get(pk=assignedCourseID)

        newQuiz = Quiz.objects.get(quizID=request.POST['quizID'])
        newQuiz.quizName = request.POST['quizName']
        newQuiz.course = assignedCourse
        newQuiz.quizData = questionsJSON
        newQuiz.save()
        
        context = {"quizObjects": Quiz.objects.all, "notification": "Successfully edited quiz", }
        return render(request, 'quizzes/manage.html', context)


    else:
        context = {"courseObjects": Course.objects.all, "quizObject": Quiz.objects.get(id=quizID), }
        return render(request, 'quizzes/edit.html', context)
    
