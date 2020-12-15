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

    anyDue = False
    for i in Quiz.objects.all():
        print(i)
        if i.isDue:
            anyDue = True

    context = {"quizObjects": Quiz.objects.all, "anyDue": anyDue}

    return render(request, 'quizzes/manage.html', context)
    



#quiz view page
@login_required
def repeatQuiz(request, quizID):

    newQuiz = Quiz.objects.get(quizID=quizID)
    
    newQuiz.pk = None
    if newQuiz.repeatNumber > 0:
        newQuiz.repeatNumber += 1
        newQuiz.quizName = newQuiz.quizName[:-1] + str(newQuiz.repeatNumber)
    else:
        newQuiz.repeatNumber = 1
        newQuiz.quizName += " repeat 1"

    if request.method == 'POST':
        
        dueDate = request.POST['dueDate']
        dueTime = request.POST['dueTime']

        dueDate += dueTime
        dueDateTime = datetime.strptime(dueDate, "%b %d, %Y%I:%M %p")
        
        newQuiz.quizDueDate = sgt.localize(dueDateTime)
        newQuiz.quizID += "r"
        newQuiz.save()
        

        anyDue = False
        for i in Quiz.objects.all():
            print(i)
            if i.isDue:
                anyDue = True
        context = {"quizObjects": Quiz.objects.all, "anyDue": anyDue, "notification": "Successfully repeated quiz"}
        return render(request, 'quizzes/manage.html', context)

    else:
        context = {"newQuizName": newQuiz.quizName}
        return render(request, 'quizzes/repeat.html', context)





#quiz creation page
@login_required
def createQuiz(request):
    nowTime = datetime.now()
    timestamp = nowTime.strftime("%Y-%m-%d-%H-%M")


    modules = Module.objects.all()
    for module in modules:
        module.tags = module.course.quizTags



    courseObjects = list(Course.objects.all())
    courseIDs = [i.id for i in courseObjects]

    context = {"quizIDtoUse": "quiz%s" % (timestamp), "courseObjects": courseObjects, "courseIDs": courseIDs ,"moduleObjects": modules, }
    
    #if submitting form
    if request.method == 'POST':
        if Quiz.objects.filter(quizID=request.POST['quizID']):
            context = {"quizObjects": Quiz.objects.all, "error": "This quiz ID is already being used, please avoid refreshing the page."}
            return render(request, 'quizzes/manage.html', context)



        questionsJSON = request.POST['allQuestionsJSON']
        questionsJSON = re.sub("_____var__", "", questionsJSON) #remove js stuff
        

        questionsJSON = json.loads(questionsJSON)
        print(questionsJSON)

        questionsJSON[0]["quizName"] = request.POST['quizName']
        
        questionsJSON = json.dumps(questionsJSON)
        
        if not "assignedModule" in request.POST or not (request.POST['dueDate']!='' and request.POST['dueTime']!='' and request.POST["assignedModule"] and request.POST["assignedModule"]!='' and request.POST['quizName']!=''):
            context = {"quizObjects": Quiz.objects.all, "error": "Please fill in all fields."}
            return render(request, 'quizzes/manage.html', context)

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
        newQuiz.repeatNumber = 0
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
        currentQuizResponses = user.quizResponses
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

        newQuiz = Quiz.objects.get(quizID=request.POST['quizID'])
        newQuiz.quizName = request.POST['quizName']
        newQuiz.quizDueDate = sgt.localize(dueDateTime)
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