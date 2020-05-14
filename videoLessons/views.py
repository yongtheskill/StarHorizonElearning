from django.shortcuts import render

# Management page
def manageVideoLessons(request):

    return render(request, 'videoLessons/manage.html')
