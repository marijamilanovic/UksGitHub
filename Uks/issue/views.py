from email import message
from hashlib import new
from imp import reload
from operator import contains
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from comment.models import EMOJI_PICKER, Emoji
from pickle import FALSE, TRUE

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
from datetime import datetime, timedelta
from history.models import History
from comment.models import Comment

from django.contrib import messages
from django.db.models import Q

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


@login_required(login_url="login")
def add_issue(request):
    d = datetime.today() - timedelta(hours=1)
    if request.method == 'POST':
        repository = get_object_or_404(Repository, id = request.POST['repository'])
        new_issue = Issue(
            issue_title = request.POST['title'], 
            description = request.POST['description'], 
            repository = repository, 
            opened_by = request.user.username,
            created = d)
        # history changes - title  and description
        message = 'added title and description'
        history = History(user = request.user,message = message, created_date = d, changed_object_id = request.user.id, object_type= 'Issue_changes')
        history.save()
        new_issue.save()
        new_issue.history.add(history)
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
    emojis = list()
    for e in EMOJI_PICKER:
        emojis.append(e[0])
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
        'labels': get_labels_by_repo(repository),
        'comments': issue.comments.all().order_by('created_date'),
        'emojis': emojis
        })


@login_required(login_url="login")
def update_issue(request, id):
    if request.method == 'POST':
        issue = get_issue_by_id(id)
        d = datetime.today() - timedelta(hours=1)
        if issue.issue_title != request.POST['title']:
            # history changes - title
            message = 'changed title'
            history = History(user = request.user,message = message, created_date = d, changed_object_id = request.user.id, object_type= 'Issue_changes')
            history.save()
            issue.save()
            issue.history.add(history)
            issue.issue_title = request.POST['title']
        if issue.description != request.POST['description']:
            # history changes - description
            message = 'changed description'
            history = History(user = request.user,message = message, created_date = d, changed_object_id = request.user.id, object_type= 'Issue_changes')
            history.save()
            issue.save()
            issue.history.add(history)
            issue.description = request.POST['description']
        if issue.state != request.POST['state']:
            # history changes - state
            message = 'changed state to ' + str(request.POST['state'])
            history = History(user = request.user,message = message, created_date = d, changed_object_id = request.user.id, object_type= 'Issue_changes')
            history.save()
            issue.save()
            issue.history.add(history)
            issue.state = request.POST['state']
        issue = add_milestone_in_issue(request, issue)
        issue.save()
        issue = add_projects_in_issue(request, issue)
        issue = add_assignees_in_issue(request, issue)
        issue = add_pullrequests_in_issue(request, issue)
        issue = add_labels_in_issue(request, issue)
        messages.success(request, 'Issue has been updated.')
        return issues(request, issue.repository.id)


@login_required(login_url="login")
def delete_issue(request, id):
    issue = get_object_or_404(Issue, id=id)
    if not issue.repository.developers.all().filter(id=request.user.id):
        return HttpResponse('401 Unauthorized', status=401)
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
    d = datetime.today() - timedelta(hours=1)
    if usernames:
        for old_username in issue.assignees.all():
            if not str(old_username) in usernames:      # obrisan element
                old_user = get_object_or_404(User, username = old_username)
                issue.assignees.remove(old_user.id)
                message = 'unassigned'
                # history changed
                print("ne treba")
                history = History(user = request.user,message= message, created_date = d, changed_object_id = old_user.id, object_type= 'Issue_assignee')
                history.save()
                issue.save()
                issue.history.add(history)
        for username in usernames:                 # novi element
            new_developer = get_object_or_404(User, username = username)
            message = 'assigned'
            if not new_developer in issue.assignees.all():
                # history changed
                history = History(user = request.user,message = message, created_date = d, changed_object_id = new_developer.id, object_type= 'Issue_assignee')
                history.save()
                issue.save()
                issue.history.add(history)
                issue.assignees.add(new_developer)
    elif issue.assignees.all() and len(usernames) == 0:
        for old_username in issue.assignees.all():
            old_user = get_object_or_404(User, username = old_username)
            message = 'unassigned'
            # history changed
            history = History(user = request.user,message = message, created_date = d, changed_object_id = old_user.id, object_type= 'Issue_assignee')
            history.save()
            issue.history.add(history)
            issue.save()
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
    return Project.objects.filter(Q(repository = repository) and Q(status = 'Opened'))

def add_projects_in_issue(request, issue):
    d = datetime.today() - timedelta(hours=1)
    projects_ids = request.POST.getlist('projects_ids')
    projects_ids = [ int(x) for x in projects_ids ]
    if projects_ids:
        for old_project in issue.projects.all():
            if not old_project.id in projects_ids:      # obrisan element
                message = 'removed issue from project'
                # history changed
                history = History(user = request.user,message = message, created_date = d, changed_object_id = old_project.id, object_type= 'Issue_project')
                history.save()
                issue.history.add(history)
                issue.save()
                issue.projects.remove(old_project.id)
        for project_id in projects_ids:                 # novi element
            new_project = get_object_or_404(Project, id = project_id)
            if not new_project in issue.projects.all():
                message = 'added issue to project'
                # history changed
                history = History(user = request.user,message = message, created_date = d, changed_object_id = new_project.id, object_type= 'Issue_project')
                history.save()
                issue.history.add(history)
                issue.save()
                issue.projects.add(new_project)
    elif issue.projects.all() and not projects_ids:
        for old_project in issue.projects.all():
            message = 'removed issue from project'
            # history changed
            history = History(user = request.user,message = message, created_date = d, changed_object_id = old_project.id, object_type= 'Issue_project')
            history.save()
            issue.history.add(history)
            issue.save()
        issue.projects.clear()
    return issue

# milestone methods
def get_milestones_by_issue_repo(id):
    issue = get_issue_by_id(id)
    repository = get_object_or_404(Repository, id = issue.repository.id)
    return Milestone.objects.all().filter(repository=repository)

def add_milestone_in_issue(request, issue):
    d = datetime.today() - timedelta(hours=1)
    if not request.POST.getlist('milestone_id'):
        if issue.milestone != None:
            message = 'removed this from the milestone'
            # history changed
            history = History(user = request.user,message = message, created_date = d, changed_object_id = issue.milestone.id, object_type= 'Issue_milestone')
            history.save()
            issue.history.add(history)
            issue.milestone = None
            issue.save()
        return issue
    elif issue.milestone != None:
        if issue.milestone.id == request.POST.getlist('milestone_id')[0]:
            return issue
    elif issue.milestone == None:
        return issue
    elif issue.milestone.id != Milestone.objects.get(id = request.POST.getlist('milestone_id')[0]):
        issue.milestone = Milestone.objects.get(id = request.POST.getlist('milestone_id')[0])
        message = 'added this from the milestone'
        # history changed
        history = History(user = request.user,message = message, created_date = d, changed_object_id = issue.milestone.id, object_type= 'Issue_milestone')
        history.save()
        issue.history.add(history)
        issue.save()
    return issue

# pullrequests methods
def get_pullrequests_by_repo(repository):
    return Pullrequest.objects.filter(prRepository = repository)

def add_pullrequests_in_issue(request, issue):
    d = datetime.today() - timedelta(hours=1)
    pullrequests_ids = request.POST.getlist('pullrequests_ids')
    pullrequests_ids = [ int(x) for x in pullrequests_ids ]
    if pullrequests_ids:
        for old_pullrequest in issue.pullrequests.all():
            if not old_pullrequest.id in pullrequests_ids:      # obrisan element
                message = 'removed pullrequest'
                # history changed
                history = History(user = request.user,message = message, created_date = d, changed_object_id = old_pullrequest.id, object_type= 'Issue_pullrequest')
                history.save()
                issue.history.add(history)
                issue.save()
                issue.pullrequest.remove(old_pullrequest.id)
        for pullrequest_id in pullrequests_ids:                 # novi element
            new_pullrequest = get_object_or_404(Pullrequest, id = pullrequest_id)
            if not new_pullrequest in issue.pullrequests.all():
                message = 'added pullrequest'
                # history changed
                history = History(user = request.user,message = message, created_date = d, changed_object_id = new_pullrequest.id, object_type= 'Issue_pullrequest')
                history.save()
                issue.history.add(history)
                issue.save()
                issue.pullrequests.add(new_pullrequest)
    elif issue.pullrequests.all() and not pullrequests_ids:
        for old_pullrequest in issue.pullrequests.all():
            message = 'removed pullrequest'
            # history changed
            history = History(user = request.user,message = message, created_date = d, changed_object_id = old_pullrequest.id, object_type= 'Issue_pullrequest')
            history.save()
            issue.history.add(history)
            issue.save()
        issue.pullrequests.clear()
    return issue

# labels methods
def get_labels_by_repo(repository):
    return Label.objects.filter(repository = repository)

def add_labels_in_issue(request, issue):
    d = datetime.today() - timedelta(hours=1)
    labels_ids = request.POST.getlist('labels_ids')
    labels_ids = [ int(x) for x in labels_ids ]
    if labels_ids:
        for old_label in issue.labels.all():
            if not old_label.id in labels_ids:      # obrisan element
                message = 'removed label'
                # history changed
                history = History(user = request.user,message = message, created_date = d, changed_object_id = old_label.id, object_type= 'Issue_label')
                history.save()
                issue.history.add(history)
                issue.save()
                issue.labels.remove(old_label.id)
        for label_id in labels_ids:                 # novi element
            new_label = get_object_or_404(Label, id = label_id)
            if not new_label in issue.labels.all():
                message = 'added label'
                # history changed
                history = History(user = request.user,message = message, created_date = d, changed_object_id = new_label.id, object_type= 'Issue_label')
                history.save()
                issue.history.add(history)
                issue.save()
                issue.labels.add(new_label)
    elif issue.labels.all() and not labels_ids:
        for old_label in issue.labels.all():
            message = 'removed label'
            # history changed
            history = History(user = request.user,message = message, created_date = d, changed_object_id = old_label.id, object_type= 'Issue_label')
            history.save()
            issue.history.add(history)
            issue.save()
        issue.labels.clear()
    return issue


def can_user_access_private_repo(request, repository):
    if request.user.id == repository.creator_id  or repository.developers.all().filter(id=request.user.id):
        return True

def add_comment_issue(request, id):
    d = datetime.today() - timedelta(hours=1)
    content = request.POST.get('comment')
    issue = get_object_or_404(Issue, id=id)
    errorTitle = None
    emojis = list()
    for e in EMOJI_PICKER:
        emojis.append(e[0])
    if content is None:
        errorTitle = "You must enter comment content."
        return view_issue(request, id)
    else:     
        if request.method == 'POST':
            comment = Comment(author = request.user, content = content, created_date = d)
            comment.save()
            issue.comments.add(comment)
            issue.save()
            return view_issue(request, id)


def add_emoji_issue(request, id, pr_id):
    if request.method == 'POST':
        have_emoji = FALSE
        emoji = Emoji()
        comment = get_object_or_404(Comment, id=id)
        emojis = comment.emojis.all()
        
        for e in emojis:
            if e.name == request.POST.get('emoji'):
                have_emoji = TRUE
                emoji = e
                
        if have_emoji == TRUE:
            add_reaction_creator(request, comment, emoji)
        else:
            create_new_emoji(request, comment)

        return view_issue(request, pr_id)

def add_reaction_creator(request, comment, emoji):
    reaction_creators = emoji.reaction_creators.all()
    for r in reaction_creators:
        if r.id == request.user.id:
            emoji.reaction_creators.remove(request.user.id)
            if len( emoji.reaction_creators.all()) == 0:
                comment.emojis.remove(emoji.id)
                comment.save()
        else:
            emoji.reaction_creators.add(request.user)

def delete_comment_issue(request, id, pr_id):
    comment = get_object_or_404(Comment, id=id)
    issue = get_object_or_404(Issue, id=pr_id)

    issue.comments.remove(comment.id)
    issue.save()
    emojis = comment.emojis.all()
    for e in emojis:
        emoji = get_object_or_404(Emoji, id=e.id)
        emoji.delete()
    comment.delete()

    return view_issue(request, issue.id)

def create_new_emoji(request, comment):
    emoji = Emoji()
    emoji.name = request.POST.get('emoji')
    emoji.save()
    user = request.user
    emoji.reaction_creators.add(user)
    emoji.save()
    comment.emojis.add(emoji)
    comment.save()