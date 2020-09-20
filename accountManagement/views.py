from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .models import User, Course, StudentClass, Module
from videoLessons.models import Video
from quizzes.models import Quiz
from fileUploads.models import FileUpload
from liveLesson.models import LiveLesson

import pytz
sgt = pytz.timezone('Asia/Singapore')
from datetime import date, datetime, timedelta

# Create your views here.

# Login Page
def loginHome(request):
    
    if request.user.is_authenticated:
        return redirect('/')

    context = {'displayFailMessage': False}
    nextURL = request.GET.get('next')

    if request.POST:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None: 
                login(request, user)
                '''if request.user.passwordChangeRequired:
                    
                    context = {'email': request.user.email, 'phoneNumber': request.user.phoneNumber, "forcePwChange": "yes",}
                    userId = request.user.id
                    user = User.objects.get(id = userId)
                    
                    return render(request, 'core/manageAccount.html', context)'''


                if nextURL is not None:
                    return redirect(nextURL)
                else:
                    return redirect('/')
                #context = {'authStatus': "Log in success",}
                #return render(request, 'projects/home.html', context)

        else:
            context = {'displayFailMessage': True}

    return render(request, 'accountManagement/login.html', context)
    
# Logout Page
def logoutHome(request):

    if request.POST:
        logout(request)
        return redirect('/')

    return render(request, 'accountManagement/logout.html')

# Manage Account Page
@login_required
def manageAccount(request):
    context = {'email': request.user.email, 'phoneNumber': request.user.phoneNumber}
    userId = request.user.id
    user = User.objects.get(id = userId)
    if request.POST:
        user.email = request.POST['email']
        user.phoneNumber = request.POST['phoneNumber']
        user.passwordChangeRequired = False
        user.save()
        context = {'email': request.user.email, 'phoneNumber': request.user.phoneNumber, "notification": "Successfully updated details",}
        return render(request, 'accountManagement/manageAccount.html', context)
    
    return render(request, 'accountManagement/manageAccount.html', context)

# Change password page
@login_required
def changePassword(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accountManagement/changePassword.html', {'form': form})

# View list of students and teachers in class
@login_required
def classView(request, classId):

    studentClass = StudentClass.objects.get(id = classId)
    teachers = list(User.objects.filter(classes = classId, accountType = "Teacher"))
    students = list(User.objects.filter(classes = classId, accountType = "Student"))
    courses = list(studentClass.courses.all())
    liveLessonsNew, liveLessonsOld = newnessChecker( list(LiveLesson.objects.filter(studentClass = classId)) )

    context = {"class": studentClass, "teachers": teachers, "students": students, "courses": courses, "liveLessonsNew": liveLessonsNew, "liveLessonsOld": liveLessonsOld, }

    return render(request, 'accountManagement/classView.html', context)

# View list of classes participating in a course, as well as course materials
@login_required
def courseView(request, courseId):

    course = Course.objects.get(id = courseId)
    classes = list(StudentClass.objects.filter(courses = courseId))
    modules = list(Module.objects.filter(course = courseId))

    for module in modules:
        module.quizzesNew, module.quizzesOld = newnessChecker( list(Quiz.objects.filter(module = module)) )
        module.videoLessonsNew, module.videoLessonsOld = newnessChecker( list(Video.objects.filter(module = module)) )
        module.fileUploadsNew, module.fileUploadsOld = newnessChecker( list(FileUpload.objects.filter(module = module)) )


    context = {"course": course, "classes": classes, "modules": modules, }

    return render(request, 'accountManagement/courseView.html', context)

@login_required
def individualAccountView(request, userId):

    user = User.objects.get(id = userId)
    classes = list(user.classes.all())

    context = {"tempUser": user, "classes": classes, }

    return render(request, 'accountManagement/individualAccountView.html', context)

@login_required
def classListView(request):

    classes = list(request.user.classes.all())

    for studentClass in classes:

        outstandingLivelessons = list(LiveLesson.objects.filter(studentClass = studentClass, streamTime__contains = date.today()))
        
        livelessonObjs = [i for i in outstandingLivelessons if i.studentClass in classes]
        
        for course in studentClass.courses.all():
            modules = list(Module.objects.filter(course = course))

            for module in modules:
                outstandingQuizzes = list(Quiz.objects.filter(module = module, quizDueDate__contains = date.today()))

    print(classes, outstandingLivelessons)

    context = {"classes": classes, "outstandingQuizzes": outstandingQuizzes, "outstandingLivelessons": outstandingLivelessons, }

    return render(request, 'accountManagement/classListView.html', context)




def newnessChecker(materialList):
    # Used in courseview page
    # Detects what course materials are new (within 2 days), places them on top of the list
    today = sgt.localize(datetime.today())
    
    timeLimit = today-timedelta(hours=48)

    oldMaterials = []
    newMaterials = []

    for material in materialList:
        if material.creationDate > timeLimit:
            newMaterials.append(material)
        else:
            oldMaterials.append(material)
    
    return newMaterials, oldMaterials
