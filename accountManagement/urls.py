from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginHome, name='Login'),
    path('logout/', views.logoutHome, name='Logout'),
    path('account/manage/', views.manageAccount, name='Manage Account'),
    path('account/manage/password', views.changePassword, name='Change Password'),
    path('class/<str:classId>/accounts', views.classView, name='Class View'),
    path('course/<str:courseId>/accounts', views.courseView, name='Course View'),
    path('course/create/<str:classId>', views.createCourse, name='Create Course'),
    path('module/create/<str:courseId>', views.createModule, name='Create Module'),
    path('account/<str:userId>', views.individualAccountView, name='Individual Account View'),
    path('classes/', views.classListView, name='Class List View'),
    path('classes/create/', views.createClass, name='Create Class'),

]