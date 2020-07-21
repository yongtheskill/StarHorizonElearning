from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .models import User, Course, StudentClass, Module
from videoLessons.models import Video
from quizzes.models import Quiz

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
        return redirect('/')
    
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

    context = {"class": studentClass, "teachers": teachers, "students": students, "courses": courses, }

    return render(request, 'accountManagement/classView.html', context)

# View list of classes participating in a course, as well as course materials
@login_required
def courseView(request, courseId):

    course = Course.objects.get(id = courseId)
    classes = list(StudentClass.objects.filter(courses = courseId))
    #quizzes = list(Quiz.objects.filter(course = courseId))
    #videoLessons = list(Video.objects.filter(course = courseId))
    modules = list(Module.objects.filter(courses = courseId))

    quizzes = {}
    videoLessons = {}

    for module in modules:
        module.quizzes = list(Quiz.objects.filter(module = module))
        module.videoLessons = list(Video.objects.filter(module = module))

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

    context = {"classes": classes, }

    return render(request, 'accountManagement/classListView.html', context)
