from django.shortcuts import render

from project.models import Project


def all_projects(request):
    all_projects = Project.objects.all()
    return render(request,'all_projects.html',{'all_projects':all_projects})
