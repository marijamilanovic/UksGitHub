from imp import reload
from django.shortcuts import render, get_object_or_404, redirect

from .models import Issue
from repository.models import Repository
from user.models import User
from milestone.models import Milestone

def issues(request, id):
    repository = get_current_repository(id)
    issues = Issue.objects.filter(repository = repository)
    return render(request, 'issues.html', {
        "issues":issues, 
        "repository":repository
        })

def all_issues(request):
    return render(request,"all_issues.html",{
        'my_issues': get_my_issues(request)
        })

def get_my_issues(request):
    issues = Issue.objects.filter(opened_by=request.user.username)
    return issues.union(Issue.objects.filter(assignee=request.user.username))

def new_issue(request, repo_id):
    repository = get_current_repository(repo_id)
    #modify users
    users = User.objects.all()
    return render(request, 'newIssue.html', {
        'repository':repository,
        'users':users, 
        'milestones': get_milestones_by_repo(repo_id)
        })

def add_issue(request):
    if request.method == 'POST':
        repository = get_object_or_404(Repository, id = request.POST['repository'] )
        if request.POST['milestone_id'] != 'empty':
            milestone = Milestone.objects.get(id = request.POST['milestone_id'])
        else:
            milestone = None
        opened_by = request.user.username
        new_issue = Issue(
            issue_title = request.POST['title'], 
            description = request.POST['description'], 
            repository = repository, 
            opened_by = opened_by)
        new_issue.save()
    return redirect('issues/' + str(repository.id))

def view_issue(request, id):
    issue = get_issue_by_id(id)
    return render(request, 'viewIssue.html',{
        'repository': get_current_repository(issue.repository.id), 
        'issue': issue, 
        'milestones': get_milestones_by_issue_repo(id), 
        'developers':get_users_by_repo(id)
        })

def update_issue(request, id):
    if request.method == 'POST':
        issue = get_issue_by_id(id)
        issue.issue_title = request.POST['title']
        issue.description = request.POST['description']
        #print(request.POST.getlist('developers'))
        if request.POST['milestone_id'] != 'empty':
            issue.milestone = Milestone.objects.get(id = request.POST['milestone_id'])
        elif issue.milestone != None:
            issue.milestone = None
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
    return render(request, "issues.html", {
        "issues":issue_update, 
        "repository":repository
        })

def view_found_issue(request, id):
    issue = get_issue_by_id(id)
    return render(request, 'viewFoundIssue.html', {
        'repository': get_current_repository(issue.repository.id), 
        'issue':issue
        })

def get_users_by_repo(id):
    issue = get_issue_by_id(id)
    repository = get_current_repository(issue.repository.id)
    return User.objects.filter(user_developers = repository)

def get_milestones_by_issue_repo(id):
    issue = get_issue_by_id(id)
    repository = get_object_or_404(Repository, id = issue.repository.id)
    return Milestone.objects.all().filter(repository=repository)

# repo methods
def get_milestones_by_repo(repo_id):
    return Milestone.objects.all().filter(repository=get_current_repository(repo_id))

def get_current_repository(repo_id):
    return get_object_or_404(Repository, id = repo_id)

# issue methods
def get_issue_by_id(id):
    return get_object_or_404(Issue, id = id)



