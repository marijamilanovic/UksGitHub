from django.shortcuts import render, get_object_or_404

from .models import Issue
from repository.models import Repository

def  issues(request, id):
    repository = get_object_or_404(Repository, id=id)
    issues = Issue.objects.filter(repository=repository)
    print(issues)
    return render(request, 'issues.html', {"issues":issues, "repository":repository})

def  issues_by_user(request):
    issues_by_user = Issue.objects.all()
    # todo: fix method
    # get all repos by logged user
    # get all issues by repo
    # get opened by logged user AND assignee
    return render(request, 'issue.html', {'issues_by_user':issues_by_user})