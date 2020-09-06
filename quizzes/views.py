from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Quiz
from accountManagement.models import Course, Module, User

import json
import re

import pytz
sgt = pytz.timezone('Asia/Singapore')
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


    modules = Module.objects.all()
    for module in modules:
        module.tags = module.courses.quizTags



    courseObjects = list(Course.objects.all())
    courseIDs = [i.id for i in courseObjects]

    context = {"quizIDtoUse": "quiz%s" % (timestamp), "courseObjects": courseObjects, "courseIDs": courseIDs ,"moduleObjects": modules, }
    
    #if submitting form
    if request.method == 'POST':
        questionsJSON = request.POST['allQuestionsJSON']
        questionsJSON = re.sub("_____var__", "", questionsJSON) #remove js stuff
        
        dueDate = request.POST['dueDate']
        dueTime = request.POST['dueTime']

        dueDate += dueTime
        dueDateTime = datetime.strptime(dueDate, "%b %d, %Y%I:%M %p")

        #find matching course
        assignedModuleID = request.POST["assignedModule"]
        assignedModule = Module.objects.get(pk=assignedModuleID)

        newQuiz = Quiz()
        newQuiz.quizName = request.POST['quizName']
        newQuiz.quizID = request.POST['quizID']
        newQuiz.quizDueDate = sgt.localize(dueDateTime)
        newQuiz.module = assignedModule
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



#quiz view page
@login_required
def doQuiz(request, quizID):
    #if submitting form
    if request.method == 'POST':
        responsesJSON = request.POST['submissionData']
        responsesJSON = re.sub("_____var__", "", responsesJSON) #remove js stuff

        userId = request.user.id
        user = User.objects.get(id = userId)
        if currentQuizResponses != None:
            currentQuizResponses = str(user.quizResponses)
        else:
            currentQuizResponses = ""
        user.quizResponses = currentQuizResponses + "__________RESPONSESPLITTER__________" + responsesJSON
        user.save()
        

        classes = list(request.user.classes.all())
        context = {"classes": classes, "notification": "Quiz Submitted", }
        return render(request, 'accountManagement/classListView.html', context)

    context = {"quizObject": Quiz.objects.get(quizID=quizID), }

    return render(request, 'quizzes/do.html', context)
    




#quiz edit page
@login_required
def editQuiz(request, quizID):
    
    #if submitting form
    if request.method == 'POST':
        questionsJSON = request.POST['allQuestionsJSON']
        questionsJSON = re.sub("_____var__", "", questionsJSON) #remove js stuff
        
        dueDate = request.POST['dueDate']
        dueTime = request.POST['dueTime']

        dueDate += dueTime
        dueDateTime = datetime.strptime(dueDate, "%b %d, %Y%I:%M %p")


        #find matching course
        assignedModID = request.POST["assignedModule"]
        assignedMod = Module.objects.get(pk=assignedModID)

        newQuiz = Quiz.objects.get(quizID=request.POST['quizID'])
        newQuiz.quizName = request.POST['quizName']
        newQuiz.quizDueDate = sgt.localize(dueDateTime)
        newQuiz.module = assignedMod
        newQuiz.quizData = questionsJSON
        newQuiz.save()
        
        context = {"quizObjects": Quiz.objects.all, "notification": "Successfully edited quiz", }
        return render(request, 'quizzes/manage.html', context)


    else:
        quizObj = Quiz.objects.get(quizID=quizID)

        dueDate = sgt.normalize(quizObj.quizDueDate).strftime("%b %d, %Y")
        dueTime = sgt.normalize(quizObj.quizDueDate).strftime("%I:%M %p")

        
        courseObjects = list(Course.objects.all())
        courseIDs = [i.id for i in courseObjects]

        context = {"courseObjects": courseObjects, "courseIDs": courseIDs ,"modObjects": Module.objects.all, "quizObject": quizObj, "dueDate": dueDate, "dueTime": dueTime, }
        return render(request, 'quizzes/edit.html', context)
    

def deleteQuiz(request):
    if request.method == 'POST':
        
        quizID = request.POST['quizID']
        quiz = Quiz.objects.get(quizID = quizID)

        quiz.delete()


        context = {"quizObjects": Quiz.objects.all, "notification": "Deleted quiz", }

        return render(request, 'quizzes/manage.html', context)

    else:
        context = {"quizObjects": Quiz.objects.all, "error": "unable to delete quiz", }

        return render(request, 'quizzes/manage.html', context)