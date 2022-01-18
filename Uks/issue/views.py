from django.shortcuts import render

from .models import Issue

def  issues(request):
    return Issue.objects.all()

def  issues_by_repo(request, id):
    issues_by_repo = Issue.objects.all()
    # todo: fix method
    return render(request, 'issue.html', {'issues_by_repo':issues_by_repo})

def  issues_by_user(request):
    issues_by_user = Issue.objects.all()
    # todo: fix method
    # get all repos by logged user
    # get all issues by repo
    # get opened by logged user AND assignee
    return render(request, 'issue.html', {'issues_by_user':issues_by_user})