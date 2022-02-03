from email import message
from hashlib import new
from imp import reload
from operator import contains
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from home.views import repository
from label.models import Label

from repository.views import collaborators


from .models import Issue
from repository.models import Repository
from user.models import User
from project.models import Project
from milestone.models import Milestone
from pullrequest.models import Pullrequest
from label.models import Label
from datetime import datetime

from django.contrib import messages
from django.db.models import Q

@login_required(login_url="login")
def issues(request, id):
    repository = get_current_repository(id)
    issues = Issue.objects.filter(repository = repository)
    assignees = load_assignees(request, id)
    milestones_for_repository = get_milestones_for_repository(repository)
    labels = Label.objects.all()
    projects = Project.objects.filter(repository = repository)
    return render(request, 'issues.html', {
        "issues":issues, 
        "repository":repository,
        "logged_user_id": request.user.id,
        "assignees":assignees,
        'milestones': milestones_for_repository,
        "labels" : labels,
        "projects":projects
        })

def empty_filter_issues(request, repo_id):
    repository = Repository.objects.get(id = repo_id)
    assignees = load_assignees(request, repo_id)
    milestones_for_repository = get_milestones_for_repository(repository)
    issues_for_return = Issue.objects.filter(repository = repository)
    labels = Label.objects.all()
    all_projects = Project.objects.filter(repository = repository)

    return render(request, 'issues.html', {
    "assignees":assignees,
    "issues":issues_for_return, 
    "repository":repository,
    "logged_user_id": request.user.id,
    "milestones": milestones_for_repository,
    "labels" : labels,
    "projects":all_projects
    })

def filter_issues(request,repo_id,pk):
    print("print")
    print(pk)
    repository = Repository.objects.get(id = repo_id)
    assignees = load_assignees(request, repo_id)
    pk = pk.strip()
    params = []
    if "," in pk:
        params = pk.split(",")
    else:
        params.append(pk)
    print(params)
    milestones_for_repository = get_milestones_for_repository(repository)
    issues_for_return = Issue.objects.filter(repository = repository)
    labels = Label.objects.all()
    all_projects = Project.objects.filter(repository = repository)
    print(pk)
    #for param in params:
    try:
        for i in range(len(params)):
            print(params[i])
            try:
                filter_type ,filter_value= params[i].split(":")
                filter_type = filter_type.strip()
                filter_value = filter_value.strip()
            except:
                filter_type = ""
            if filter_type.lower() == "title":
                issues_match_title =  Issue.objects.filter(issue_title__icontains = filter_value)
                issues_for_return = issues_for_return.intersection(issues_match_title)
            elif filter_type.lower() == "body":
                issues_match_body =  Issue.objects.filter(description__icontains = filter_value)
                issues_for_return = issues_for_return.intersection(issues_match_body)
            elif filter_type.lower() == "state":
                issues_match_state =  Issue.objects.filter(state__icontains = filter_value)
                issues_for_return = issues_for_return.intersection(issues_match_state)
            elif filter_type.lower() == "milestone":
                milestones = Milestone.objects.filter(title__icontains = filter_value)
                issues_match_milestone = list()
                for m in milestones:
                    issues_from_m = Issue.objects.filter(milestone = m)
                    for ifm in issues_from_m:
                        if ifm not in issues_match_milestone:
                            issues_match_milestone.append(ifm)            
                issues_for_return = set(issues_for_return).intersection(issues_match_milestone)
            elif filter_type.lower() == "assigned":
                user = User.objects.get(username__icontains = filter_value)
                issues_match_assigned =  Issue.objects.filter(assignees = user)
                issues_for_return = issues_for_return.intersection(issues_match_assigned)
                print("assigned")
                print(issues_for_return)
            elif filter_type.lower() == "project":
                projects = Project.objects.filter(name__icontains = filter_value)
                issues_match_projects = list()
                for p in projects:
                    issues_from_p = Issue.objects.filter(projects = p)
                    for ifp in issues_from_p:
                        if ifp not in issues_match_projects:
                            issues_match_projects.append(ifp)            
                issues_for_return = set(issues_for_return).intersection(issues_match_projects)
            elif filter_type.lower() == "label":
                print(filter_value)
                label = Label.objects.get(name__icontains = filter_value)
                issues_match_label =  Issue.objects.filter(labels = label)
                issues_for_return = issues_for_return.intersection(issues_match_label)
                print("label")
                print(issues_for_return)
            elif filter_type.lower() == "author":
                user = User.objects.get(username__icontains = filter_value)
                issues_match_author =  Issue.objects.filter(opened_by = user)
                issues_for_return = issues_for_return.intersection(issues_match_author)
            elif filter_type.lower() == "in":
                if i > 1 :
                    if filter_value.lower() == "title":
                        issues_match_title = Issue.objects.filter(issue_title__icontains = params[i-1])
                        issues_for_return = issues_for_return.intersection(issues_match_title)
                    elif filter_value.lower() == "body":
                        issues_match_body = Issue.objects.filter(description__icontains = params[i-1])
                        issues_for_return = issues_for_return.intersection(issues_match_body)
                    else:
                        issues_for_return = []  
            else :     
                filter_value = params[0]
                issues_match_other =  []
                for imo in Issue.objects.filter(repository = repository):
                    if  imo.issue_title.__contains__(filter_value)  or imo.description.__contains__(filter_value):
                        issues_match_other.append(imo)
                issues_for_return = set(issues_for_return)  .intersection(issues_match_other)
    except:
        issues_for_return = []
    return render(request, 'issues.html', {
    "assignees":assignees,
    "issues":issues_for_return, 
    "repository":repository,
    "logged_user_id": request.user.id,
    "milestones": milestones_for_repository,
    "labels" : labels,
    "projects":all_projects
    })

def get_milestones_for_repository(repository):
    return  Milestone.objects.filter(repository = repository)

def load_assignees(request, repo_id):
    reposiotry = Repository.objects.get(id = repo_id)
    assignees = reposiotry.developers
    assignees.add(reposiotry.creator)
    return assignees.all()

@login_required(login_url="login")
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

@login_required(login_url="login")
def new_issue(request, repo_id):
    repository = get_current_repository(repo_id)
    if repository.status == 'private':
        if not can_user_access_private_repo(request, repository):
            return HttpResponse('401 Unauthorized', status=401)
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
        'milestones': milestones_for_repository,
        'labels': get_labels_by_repo(repository),
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
        new_issue = add_labels_in_issue(request, new_issue)
    return redirect('issues/' + str(repository.id))

def view_issue(request, id):
    issue = get_issue_by_id(id)
    repository = get_current_repository(issue.repository.id)
    if repository.status == 'private':
        if not can_user_access_private_repo(request, repository):
            return HttpResponse('401 Unauthorized', status=401)
    return render(request, 'viewIssue.html',{
        'repository': repository, 
        'issue': issue, 
        'milestones': get_milestones_by_issue_repo(id), 
        'developers':get_users_by_repo(repository),
        'projects': get_projects_by_repo(repository),
        'pullrequests': get_pullrequests_by_repo(repository),
        'labels': get_labels_by_repo(repository)
        })

def update_issue(request, id):
    if request.method == 'POST':
        issue = get_issue_by_id(id)
        issue.issue_title = request.POST['title']
        issue.description = request.POST['description']
        issue.state = request.POST['state']
        issue = add_milestone_in_issue(request, issue)
        issue.save()
        issue = add_projects_in_issue(request, issue)
        issue = add_assignees_in_issue(request, issue)
        issue = add_pullrequests_in_issue(request, issue)
        issue = add_labels_in_issue(request, issue)
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
        for old_username in issue.assignees.all():
            if not old_username in usernames:      # obrisan element
                old_user = get_object_or_404(User, username = old_username)
                issue.assignees.remove(old_user.id)
        for username in usernames:                 # novi element
            new_developer = get_object_or_404(User, username = username)
            if not new_developer in issue.assignees.all():
                issue.assignees.add(new_developer)
    else:
        issue.assignees.clear()
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
    projects_ids = [ int(x) for x in projects_ids ]
    if projects_ids:
        for old_project in issue.projects.all():
            if not old_project.id in projects_ids:      # obrisan element
                issue.projects.remove(old_project.id)
        for project_id in projects_ids:                 # novi element
            new_project = get_object_or_404(Project, id = project_id)
            if not new_project in issue.projects.all():
                issue.projects.add(new_project)
    else:
        issue.projects.clear()
    return issue

# milestone methods
def get_milestones_by_issue_repo(id):
    issue = get_issue_by_id(id)
    repository = get_object_or_404(Repository, id = issue.repository.id)
    return Milestone.objects.all().filter(repository=repository)

def add_milestone_in_issue(request, issue):
    if not request.POST.getlist('milestone_id'):
        issue.milestone = None
        return issue
    elif issue.milestone != None:
        if issue.milestone.id == request.POST.getlist('milestone_id')[0]:
            return issue
    issue.milestone = Milestone.objects.get(id = request.POST.getlist('milestone_id')[0])
    return issue

# pullrequests methods
def get_pullrequests_by_repo(repository):
    return Pullrequest.objects.filter(prRepository = repository)

def add_pullrequests_in_issue(request, issue):
    pullrequests_ids = request.POST.getlist('pullrequests_ids')
    pullrequests_ids = [ int(x) for x in pullrequests_ids ]
    if pullrequests_ids:
        for old_pullrequest in issue.pullrequests.all():
            if not old_pullrequest.id in pullrequests_ids:      # obrisan element
                issue.pullrequest.remove(old_pullrequest.id)
        for pullrequest_id in pullrequests_ids:                 # novi element
            new_pullrequest = get_object_or_404(Pullrequest, id = pullrequest_id)
            if not new_pullrequest in issue.pullrequests.all():
                issue.pullrequests.add(new_pullrequest)
    else:
        issue.pullrequests.clear()
    return issue

# labels methods
def get_labels_by_repo(repository):
    return Label.objects.filter(repository = repository)

def add_labels_in_issue(request, issue):
    labels_ids = request.POST.getlist('labels_ids')
    labels_ids = [ int(x) for x in labels_ids ]
    if labels_ids:
        for old_label in issue.labels.all():
            if not old_label.id in labels_ids:      # obrisan element
                issue.labels.remove(old_label.id)
        for label_id in labels_ids:                 # novi element
            new_label = get_object_or_404(Label, id = label_id)
            if not new_label in issue.labels.all():
                issue.labels.add(new_label)
    else:
        issue.labels.clear()
    return issue


def can_user_access_private_repo(request, repository):
    if request.user.id == repository.creator_id  or repository.developers.all().filter(id=request.user.id):
        return True
