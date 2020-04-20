from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .models import User, Course

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

# Allows teachers to view details of all their students
@login_required
def studentView(request):

    allStudents = list(User.objects.filter(group_id = classId))
    course = Course.objects.get(id = classId)

    context = {"course": course, "Students": allStudents, }
