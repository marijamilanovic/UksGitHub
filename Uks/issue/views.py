from django.shortcuts import render, get_object_or_404

from .models import Issue
from repository.models import Repository

def  issues(request, id):
    repository = get_object_or_404(Repository, id=id)
    issues = Issue.objects.filter(repository=repository)
    print(issues)
    return render(request, 'issues.html', {"issues":issues, "repository":repository})