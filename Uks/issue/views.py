from email import message
from hashlib import new
from imp import reload
from django.shortcuts import render, get_object_or_404, redirect
from label.models import Label

from repository.views import collaborators

from .models import Issue
from repository.models import Repository
from user.models import User
from project.models import Project
from milestone.models import Milestone
from pullrequest.models import Pullrequest

from django.contrib import messages

def issues(request, id):
    repository = get_current_repository(id)
    issues = Issue.objects.filter(repository = repository)
    assignees = load_assignees(request, id)
    milestones_for_repository = get_milestones_for_repository(repository)
    return render(request, 'issues.html', {
        "issues":issues, 
        "repository":repository,
        "logged_user_id": request.user.id,
        "assignees":assignees,
        'milestones': milestones_for_repository
        })

def filter_issues_for_multiple_objects(request, repo_id, pk, object_id):
    pass

def filter_issues(request,repo_id,pk):
    repo_id = 8
    print("print")
    print(pk)
    repository = Repository.objects.get(id = repo_id)
    assignees = load_assignees(request, repo_id)

    if "," in pk:
        params = pk.split(",")
    else:
        params = []
        params.append(pk)
    print(params)
    milestones_for_repository = get_milestones_for_repository(repository)
    issues_for_return = Issue.objects.filter(repository = repository)
    for param in params:
        filter_type ,filter_value= param.split(":")
        if filter_type == "issue_title":
            issues_for_return =  Issue.objects.filter(issue_title = filter_value)
        elif filter_type == "description":
            issues_for_return =  Issue.objects.filter(description = filter_value)
        elif filter_type == "state":
            issues_for_return =  Issue.objects.filter(state = filter_value)
        elif filter_type == "milestone":
            milestone = Milestone.objects.get(id = int(filter_value))
            issues_for_return =  Issue.objects.filter(milestone = filter_value)
        elif filter_type == "assigned":
            user = User.objects.get(username = filter_value)
            issues_for_return =  Issue.objects.filter(assignees = user)
        elif filter_type == "label":
            label = Label.objects.get(id = int(filter_value))
            issues_for_return =  Issue.objects.filter(labels = label)
        elif filter_type == "author":
            user = User.objects.get(username = filter_value)
            issues_for_return =  Issue.objects.filter(opened_by = user)

    return render(request, 'issues.html', {
    "assignees":assignees,
    "issues":issues_for_return, 
    "repository":repository,
    "logged_user_id": request.user.id,
    "milestones": milestones_for_repository
    })

def get_milestones_for_repository(repository):
    return  Milestone.objects.filter(repository = repository)

def load_assignees(request, repo_id):
    print("Usao ovde")
    reposiotry = Repository.objects.get(id = repo_id)
    assignees = reposiotry.developers
    assignees.add(reposiotry.creator)
    return assignees.all()

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
    milestones_for_repository = get_milestones_for_repository(repository)
    return render(request, 'newIssue.html', {
        'repository':repository,
        'users':users, 
        'milestones': get_milestones_by_repo(repo_id),
        'projects': get_projects_by_repo(repository),
        'developers': get_users_by_repo(repository),
        'pullrequests': get_pullrequests_by_repo(repository),
        'logged_user_id': request.user.id,        
        'milestones': milestones_for_repository
        })

def add_issue(request):
    if request.method == 'POST':
        repository = get_object_or_404(Repository, id = request.POST['repository'])
        new_issue = Issue(
            issue_title = request.POST['title'], 
            description = request.POST['description'], 
            repository = repository, 
            opened_by = request.user.username)
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
    milestones_for_repository = get_milestones_for_repository(repository)
    return render(request, 'viewIssue.html',{
        'repository': repository, 
        'issue': issue, 
        'milestones': get_milestones_by_issue_repo(id), 
        'developers':get_users_by_repo(repository),
        'projects': get_projects_by_repo(repository),
        'pullrequests': get_pullrequests_by_repo(repository),
        "milestones": milestones_for_repository
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


