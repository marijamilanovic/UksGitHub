from imp import reload
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
        'repository':repository,
        'users':users})

def add_issue(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        repository = get_object_or_404(Repository, id = request.POST['repository'] )
        opened_by = request.user.username
        new_issue = Issue(issue_title = title, description = description, repository = repository, opened_by = opened_by)
        new_issue.save()
    return redirect('issues/' + str(repository.id))

def view_issue(request, id):
    issue = get_object_or_404(Issue, id = id)
    repository = get_object_or_404(Repository, id = issue.repository.id)
    return render(request, 'viewIssue.html', {'repository': repository, 'issue':issue})

def update_issue(request, id):
    if request.method == 'POST':
        issue = get_object_or_404(Issue, id = id)
        issue.issue_title = request.POST['title']
        issue.description = request.POST['description']
        all_repos = Repository.objects.all()
        for r in all_repos:
            if(r.id == issue.repository.id):
                repository = r
        issue.save()
        return issues(request, repository.id)

def delete_issue(request, id):
    issue = get_object_or_404(Issue, id=id)
    all_repos = Repository.objects.all()
    for r in all_repos:
        if(r.id == issue.repository.id):
            repository = r
    issue.delete()
    issue_update = Issue.objects.filter(repository=issue.repository)
    return render(request, "issues.html", {"issues":issue_update, "repository":repository})

def view_found_issue(request, id):
    issue = get_object_or_404(Issue, id = id)
    repository = get_object_or_404(Repository, id = issue.repository.id)
    return render(request, 'viewFoundIssue.html', {'repository': repository, 'issue':issue})
