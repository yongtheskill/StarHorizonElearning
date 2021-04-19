from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Quiz
from accountManagement.models import Course, Module, User

import json
import re

import base64

import pytz
sgt = pytz.timezone('Asia/Singapore')
from datetime import datetime



#quiz management page
@login_required
def manageQuizzes(request):

    anyDue = False
    for i in Quiz.objects.all():
        if i.isDue:
            anyDue = True

    context = {"quizObjects": Quiz.objects.all, "anyDue": anyDue}

    return render(request, 'quizzes/manage.html', context)
    



#quiz view page
@login_required
def repeatQuiz(request, quizID):

    newQuiz = Quiz.objects.get(quizID=quizID)
    
    newQuiz.pk = None
    if newQuiz.repeatNumber > 3:
        anyDue = False
        for i in Quiz.objects.all():
            if i.isDue:
                anyDue = True
        context = {"quizObjects": Quiz.objects.all, "anyDue": anyDue, "error": "You cannot repeat a quiz more than 3 times."}
        return render(request, 'quizzes/manage.html', context)
    elif newQuiz.repeatNumber > 0:
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
        module.tags = list(set(list(module.course.quizTags.split(","))))



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
        if 'passingScore' in request.POST and request.POST['passingScore'] != '':
            newQuiz.passingScore = int(request.POST['passingScore'])
        else:
            newQuiz.passingScore = 0
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

        score = len(re.findall(r'"isCorrect":true', responsesJSON))

        responsesJSON = json.loads(responsesJSON)
        
        quizObj = Quiz.objects.get(quizName=responsesJSON[0]["quizName"])
        passingScore = quizObj.passingScore
        if score >= int(passingScore):
            responsesJSON[0]["isPassed"] = True
        else:
            responsesJSON[0]["isPassed"] = False
        
        responsesJSON = json.dumps(responsesJSON)

        userId = request.user.id
        user = User.objects.get(id = userId)
        currentQuizResponses = user.quizResponses

        if currentQuizResponses and "__________RESPONSESPLITTER__________" in currentQuizResponses:
            allQuizResponses = currentQuizResponses.split("__________RESPONSESPLITTER__________")[1:]
            for i in allQuizResponses:
                quizName = ""
                try:
                    quizName = json.loads(i)[0]["quizName"]
                    print(quizObj.quizName)
                    if quizName == quizObj.quizName:
                        return redirect("./")
                except:
                    pass

        if currentQuizResponses != None:
            currentQuizResponses = str(user.quizResponses)
        else:
            currentQuizResponses = ""
        user.quizResponses = currentQuizResponses + "__________RESPONSESPLITTER__________" + responsesJSON


        user.save()
        

        return redirect("./")

    quizObj = Quiz.objects.get(quizID=quizID)

    #if quizObj.quizDueDate > sgt.localize(datetime.now()):
    context = {"quizObject": Quiz.objects.get(quizID=quizID), }

    user = request.user
    quizResponseJSON = user.quizResponses
    if quizResponseJSON and "__________RESPONSESPLITTER__________" in quizResponseJSON:
        allQuizResponses = quizResponseJSON.split("__________RESPONSESPLITTER__________")[1:]
        for i in allQuizResponses:
            if quizObj.quizName == json.loads(i)[0]["quizName"]:
                #quiz done already

                
                def searchForQn(questions, questionID):
                    for i in questions:
                        if i["questionID"] == questionID:
                            return i




                quizObjToCombine = json.loads(Quiz.objects.get(quizID=quizID).quizData)

                quizResponsesToCombine = json.loads(i)[1:]

                for j in quizObjToCombine:
                    j.update(searchForQn(quizResponsesToCombine, j["questionID"]))


                context = {"quizObject": Quiz.objects.get(quizID=quizID), "responsesObject": json.dumps(quizObjToCombine), }
                return render(request, 'quizzes/viewAns.html', context)
    return render(request, 'quizzes/do.html', context)
"""
    else:
        classes = list(request.user.classes.all())
        context = {"classes": classes, "error": "Quiz is over.", }
        return render(request, 'accountManagement/classListView.html', context)
        """









@login_required
def viewQuizAns(request, quizNameEncoded, userId):   
    quizName = base64.b64decode(quizNameEncoded).decode('utf-8')

    quizObj = Quiz.objects.get(quizName=quizName)

    user = User.objects.get(id = userId)
    quizResponseJSON = user.quizResponses
    if quizResponseJSON and "__________RESPONSESPLITTER__________" in quizResponseJSON:
        allQuizResponses = quizResponseJSON.split("__________RESPONSESPLITTER__________")[1:]
        for i in allQuizResponses:
            if quizObj.quizName == json.loads(i)[0]["quizName"]:
                #quiz done already

                
                def searchForQn(questions, questionID):
                    for i in questions:
                        if i["questionID"] == questionID:
                            return i




                quizObjToCombine = json.loads(quizObj.quizData)

                quizResponsesToCombine = json.loads(i)[1:]

                for j in quizObjToCombine:
                    j.update(searchForQn(quizResponsesToCombine, j["questionID"]))


                context = {"quizObject": quizObj, "responsesObject": json.dumps(quizObjToCombine), }
                return render(request, 'quizzes/viewAns.html', context)
    else:
        return doQuiz(request, quizObj.quizID)













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
        if 'passingScore' in request.POST and request.POST['passingScore'] != '':
            newQuiz.passingScore = int(request.POST['passingScore'])
        else:
            newQuiz.passingScore = 0
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

        passingScore = quizObj.passingScore

        
        courseObjects = list(Course.objects.all())
        courseIDs = [i.id for i in courseObjects]

        context = {"courseObjects": courseObjects, "courseIDs": courseIDs ,"modObjects": Module.objects.all, "quizObject": quizObj, "dueDate": dueDate, "dueTime": dueTime, "passingScore": passingScore}
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