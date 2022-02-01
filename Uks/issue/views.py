from email import message
from hashlib import new
from imp import reload
from django.shortcuts import render, get_object_or_404, redirect

from .models import Issue
from repository.models import Repository
from user.models import User
from project.models import Project
from milestone.models import Milestone
from pullrequest.models import Pullrequest
from datetime import datetime

from django.contrib import messages

def issues(request, id):
    repository = get_current_repository(id)
    issues = Issue.objects.filter(repository = repository)
    return render(request, 'issues.html', {
        "issues":issues, 
        "repository":repository,
        "logged_user_id": request.user.id
        })

def all_issues(request):
    return render(request,"all_issues.html",{
        'my_issues': get_my_issues(request)
        })

def get_my_issues(request):
    issues = Issue.objects.filter(opened_by=request.user.username)
    assignee_issues = Issue.objects.filter(assignees = request.user.id)
    if not assignee_issues:
        return issues
    else:
        return assignee_issues.union(issues)

def new_issue(request, repo_id):
    repository = get_current_repository(repo_id)
    users = User.objects.all()
    return render(request, 'newIssue.html', {
        'repository':repository,
        'users':users, 
        'milestones': get_milestones_by_repo(repo_id),
        'projects': get_projects_by_repo(repository),
        'developers': get_users_by_repo(repository),
        'pullrequests': get_pullrequests_by_repo(repository),
        'logged_user_id': request.user.id
        })

def add_issue(request):
    if request.method == 'POST':
        repository = get_object_or_404(Repository, id = request.POST['repository'])
        new_issue = Issue(
            issue_title = request.POST['title'], 
            description = request.POST['description'], 
            repository = repository, 
            opened_by = request.user.username,
            created = datetime.now())
        new_issue = add_milestone_in_issue(request, new_issue)
        new_issue.save()
        messages.success(request, 'Issue has been created.')
        new_issue = add_assignees_in_issue(request, new_issue)
        new_issue = add_projects_in_issue(request, new_issue)
        new_issue = add_pullrequests_in_issue(request, new_issue)
    return redirect('issues/' + str(repository.id))

def view_issue(request, id):
    issue = get_issue_by_id(id)
    repository = get_current_repository(issue.repository.id)
    return render(request, 'viewIssue.html',{
        'repository': repository, 
        'issue': issue, 
        'milestones': get_milestones_by_issue_repo(id), 
        'developers':get_users_by_repo(repository),
        'projects': get_projects_by_repo(repository),
        'pullrequests': get_pullrequests_by_repo(repository)
        })

def update_issue(request, id):
    if request.method == 'POST':
        issue = get_issue_by_id(id)
        issue.issue_title = request.POST['title']
        issue.description = request.POST['description']
        issue.state = request.POST['state']
        issue = add_milestone_in_issue(request, issue)
        issue.save()
        issue.projects.clear()
        issue = add_projects_in_issue(request, issue)
        issue.assignees.clear()
        issue = add_assignees_in_issue(request, issue)
        issue.pullrequests.clear()
        issue = add_pullrequests_in_issue(request, issue)
        messages.success(request, 'Issue has been updated.')
        return issues(request, issue.repository.id)

def delete_issue(request, id):
    issue = get_object_or_404(Issue, id=id)
    all_repos = Repository.objects.all()
    for r in all_repos:
        if(r.id == issue.repository.id):
            repository = r
    issue.delete()
    messages.success(request, 'Issue has been deleted.')
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

# assignee methods
def get_users_by_repo(repository):
    return User.objects.filter(user_developers = repository)

def add_assignees_in_issue(request, issue):
    usernames = request.POST.getlist('developers')
    if usernames:
        for username in usernames:
            user = get_object_or_404(User, username = username)
            issue.assignees.add(user)
    return issue

# repo methods
def get_milestones_by_repo(repo_id):
    return Milestone.objects.all().filter(repository=get_current_repository(repo_id))

def get_current_repository(repo_id):
    return get_object_or_404(Repository, id = repo_id)

# issue methods
def get_issue_by_id(id):
    return get_object_or_404(Issue, id = id)

# project methods
def get_projects_by_repo(repository):
    return Project.objects.filter(repository = repository)

def add_projects_in_issue(request, issue):
    projects_ids = request.POST.getlist('projects_ids')
    if projects_ids:
        for project_id in projects_ids:
            project = get_object_or_404(Project, id = project_id)
            issue.projects.add(project)
    return issue

# milestone methods
def get_milestones_by_issue_repo(id):
    issue = get_issue_by_id(id)
    repository = get_object_or_404(Repository, id = issue.repository.id)
    return Milestone.objects.all().filter(repository=repository)

def add_milestone_in_issue(request, issue):
    if request.POST['milestone_id'] != 'empty':
        issue.milestone = Milestone.objects.get(id = request.POST['milestone_id'])
    elif issue.milestone != None:
        issue.milestone = None
    return issue

# pullrequests methods
def get_pullrequests_by_repo(repository):
    return Pullrequest.objects.filter(prRepository = repository)

def add_pullrequests_in_issue(request, issue):
    pullrequests_ids = request.POST.getlist('pullrequests_ids')
    if pullrequests_ids:
        for pullrequest_id in pullrequests_ids:
            pullrequest = get_object_or_404(Pullrequest, id = pullrequest_id)
            issue.pullrequests.add(pullrequest)
    return issue



