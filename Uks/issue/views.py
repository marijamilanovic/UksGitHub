from django.shortcuts import render, get_object_or_404, redirect

from .models import Issue
from repository.models import Repository
from user.models import User

def issues(request, id):
    repository = get_object_or_404(Repository, id=id)
    issues = Issue.objects.filter(repository=repository)
    print(issues)
    return render(request, 'issues.html', {"issues":issues, "repository":repository})

def new_issue(request, id):
    repository = get_object_or_404(Repository, id=id)
    users = User.objects.all()
    return render(request, 'newIssue.html', {
        "repository":repository,
        'users':users})

def add_issue(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        repository = get_object_or_404(Repository, id = request.POST['repository'] )
        new_issue = Issue(issue_title=title, description = description, repository = repository)
        new_issue.save()
    return redirect('issues/' + str(repository.id))