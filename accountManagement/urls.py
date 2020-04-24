from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginHome, name='Login'),
    path('logout/', views.logoutHome, name='Logout'),
    path('account/manage/', views.manageAccount, name='Manage Account'),
    path('account/manage/password', views.changePassword, name='Change Password'),
    path('class/accounts/students/<str:classId>', views.studentView, name='Student Account List View'),

]