from cProfile import label
from random import choices
from sqlite3 import connect
from xml.etree.ElementTree import Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from project.models import Project
from repository.views import collaborators
from .models import MERGED, PULL_REQUEST_STATE, Pullrequest, Repository, Branch
from comment.models import EMOJI_PICKER
from datetime import date
from label.models import Label
from milestone.models import Milestone
from issue.models import Issue

def pullrequests(request, id):
    repository = get_object_or_404(Repository, id=id)
    pullrequests = Pullrequest.objects.all().filter(prRepository=repository)
    my_pullrequests = []
    for pr in pullrequests:
        if pr.creator == request.user:
            my_pullrequests.append(pr)
    pullrequests_for_review = get_pullrequests_for_review(request, repository)
    return render(request, 'pullrequests.html', {"pullrequests":my_pullrequests, "repository":repository,'pullrequests_for_review':pullrequests_for_review,"logged_user_id":request.user.id})

def get_pullrequests_for_review(request, repository):
    pullrequests_for_this_repository = Pullrequest.objects.all().filter(prRepository = repository)
    pullrequests_for_review = []
    for pullrequest in pullrequests_for_this_repository:
        if request.user in pullrequest.reviewers.all() and request.user != pullrequest.creator:
            pullrequests_for_review.append(pullrequest)
    return pullrequests_for_review

def newPullrequest(request, id):
    repository = get_object_or_404(Repository, id=id)
    branches = Branch.objects.all().filter(repository=repository)
    return render(request, 'newPullrequest.html', {"branches":branches, "repository":repository, "logged_user_id": request.user.id})

def addPullrequest(request):
    if request.method == 'POST':
        created = date.today()
        prRepository = get_object_or_404(Repository, id = request.POST['repository'] )
        source = get_object_or_404(Branch, id = request.POST['branch_source_id'] )
        target = get_object_or_404(Branch, id = request.POST['branch_target_id'] )
        name = target.name
        newPullrequest = Pullrequest(name = name, status = 'Opened', created = created, prRepository = prRepository, source = source, target = target)
        newPullrequest.creator = request.user
        newPullrequest.save()
        reviewers = add_reviewrs(request, newPullrequest)
        not_assigned_collaborators_on_repository = get_not_assigned_collaborators_on_pull_request(request, reviewers, prRepository)
    return redirect('/pullrequest/updatePullrequestPage/'+ str(newPullrequest.id))

def updatePullrequestPage(request, id):
    pullrequest, repository, comments, emojis, not_assigned_collaborators_on_repository, reviewers, labels, milestones, projects, issues, connected_issues, assignees = pull_request_page_data(request, id)
    return render(request, "updatePullrequest.html", {
        'reviewers': reviewers, 
        'not_assigned_collaborators_on_repository': not_assigned_collaborators_on_repository,
        "pullrequest": pullrequest, 
        "repository": repository, 
        "comments": comments, 
        "emojis": emojis,
        "labels": labels,
        "milestones": milestones,
        "projects": projects,
        "issues": issues,
        "connected_issues": connected_issues,
        "assignees": assignees,
        "logged_user_id": request.user.id})

def get_not_assigned_collaborators_on_pull_request(request,reviewers,prRepository):
    collaborators_on_repository = User.objects.all().filter(user_developers = prRepository).all()
    not_assigned_collaborators_on_repository = []
    for collab in collaborators_on_repository:
        if collab not in reviewers and collab.id != request.user.id:
            not_assigned_collaborators_on_repository.append(collab)
    return not_assigned_collaborators_on_repository

def pull_request_page_data(request,id):
    pullrequest = get_object_or_404(Pullrequest, id = id)
    repository = get_object_or_404(Repository, id = pullrequest.prRepository.id)
    comments = pullrequest.comments.all()
    emojis = list()
    for e in EMOJI_PICKER:
        emojis.append(e[0])
    reviewers = add_reviewrs(request, pullrequest)
    not_assigned_collaborators_on_repository = get_not_assigned_collaborators_on_pull_request(request, reviewers.all(),repository)
    labels = Label.objects.all().filter(repository = repository)
    milestones = Milestone.objects.all().filter(repository = repository)
    projects = Project.objects.all().filter(repository = repository)
    issues = Issue.objects.all().filter(repository = repository)
    connected_issues = get_connected_issues_to_pull_request(id, issues)
    assignees =  repository.developers
    return pullrequest, repository, comments, emojis, not_assigned_collaborators_on_repository, reviewers, labels, milestones, projects, issues, connected_issues, assignees

def changeStatusPullrequest(request, id):
    pullrequest = get_object_or_404(Pullrequest, id = id)
    if(pullrequest.status=='Closed'):
        pullrequest.status = 'Opened'
    elif(pullrequest.status=='Opened'):
        pullrequest.status = 'Closed'
    pullrequest.save()
    return redirect('/pullrequest/pullrequests/'+str(pullrequest.prRepository.id))

def add_reviewers_on_pull_request(request, id):
    pullrequest, repository, comments, emojis, _ , _ = pull_request_page_data( request, id)
    reviewers = add_reviewrs(request, pullrequest)
    not_assigned_collaborators_on_repository = get_not_assigned_collaborators_on_pull_request(request, reviewers, repository)
    return render(request, "updatePullrequest.html", {'reviewers': reviewers, 'not_assigned_collaborators_on_repository': not_assigned_collaborators_on_repository, "pullrequest": pullrequest, "repository": repository, "comments":comments, "emojis":emojis})

def add_reviewrs(request,pullrequest):
    reviewers = request.POST.getlist('developers')
    if reviewers != None:
        for reviewer in reviewers:
            object_reviewer = User.objects.get(username = reviewer)
            if object_reviewer not in pullrequest.reviewers.all():
                pullrequest.reviewers.add(object_reviewer)
    return pullrequest.reviewers.all()

def remove_reviewer_from_pullrequest(request, pullrequest_id, reviewer_id):
    pull_request = Pullrequest.objects.get(id = pullrequest_id)
    reviewer = User.objects.get(id = reviewer_id)
    if reviewer in pull_request.reviewers.all():
        pull_request.reviewers.remove(reviewer)
    pullrequest, repository, comments, emojis, not_assigned_collaborators_on_repository, reviewers, labels, milestones, projects, issues, connected_issues, assignees = pull_request_page_data(request, pullrequest_id)
    return render(request, "updatePullrequest.html", {
        'reviewers': reviewers, 
        'not_assigned_collaborators_on_repository': not_assigned_collaborators_on_repository,
        "pullrequest": pullrequest, 
        "repository": repository, 
        "comments": comments, 
        "emojis": emojis,
        "labels": labels,
        "milestones": milestones,
        "projects": projects,
        "issues": issues,
        "connected_issues": connected_issues,
        "assignees": assignees})

def approve(request, pullrequest_id):
    pullrequest = Pullrequest.objects.get(id = pullrequest_id)
    repository = pullrequest.prRepository
    pullrequests = Pullrequest.objects.all().filter(prRepository=repository)
    my_pullrequests = []
    for pr in pullrequests:
        if pr.creator == request.user:
            my_pullrequests.append(pr)
    repository = pullrequest.prRepository
    reviewer = request.user
    if reviewer in pullrequest.reviewers.all():
        pullrequest.reviewers.remove(reviewer)
        pullrequest.reviewed = True
        pullrequest.save()
    pullrequests_for_review = get_pullrequests_for_review(request, repository)
    return render(request, 'pullrequests.html', {"pullrequests":my_pullrequests, "repository":repository,'pullrequests_for_review':pullrequests_for_review})

def merge(request, pullrequest_id):
    pullrequest = Pullrequest.objects.get(id = pullrequest_id)
    repository = pullrequest.prRepository
    try_merge(pullrequest)
    pullrequests = Pullrequest.objects.all().filter(prRepository=repository)
    my_pullrequests = []
    for pr in pullrequests:
        if pr.creator == request.user:
            my_pullrequests.append(pr)
    pullrequests_for_review = get_pullrequests_for_review(request, repository)
    return render(request, 'pullrequests.html', {"pullrequests":my_pullrequests, "repository":repository,'pullrequests_for_review':pullrequests_for_review})

def try_merge(pullrequest):
    if len(pullrequest.reviewers.all()) == 0 and pullrequest.reviewed:
        pullrequest.status = "Merged"
        pullrequest.save()
        return True
    return False

def add_assignees_on_pull_request(request, id):
    pullrequest = get_object_or_404(Pullrequest, id=id)
    assignees = request.POST.getlist('assignees')

    for a in assignees:
        for e in pullrequest.assignees.all():
            if a == e.username:
                pullrequest.assignees.remove(e.id)
                pullrequest.save()
                assignees.remove(a)
    print(pullrequest.prRepository.id)
    for a in assignees:
        user = get_object_or_404(User, username=a)
        pullrequest.assignees.add(user)
        pullrequest.save()
        
    return redirect('/pullrequest/updatePullrequestPage/'+ str(id))


def delete_assignees_on_pull_request(request, id, assignee_id):
    pullrequest = get_object_or_404(Pullrequest, id=id)
    pullrequest.assignees.remove(assignee_id)
    pullrequest.save()

    return redirect('/pullrequest/updatePullrequestPage/'+ str(id))


def add_labels_on_pull_request(request, id):
    pullrequest = get_object_or_404(Pullrequest, id=id)
    labels = request.POST.getlist('labels')

    for label in labels:
        for l in pullrequest.labels.all():
            if label == l.id:
                pullrequest.assignees.remove(l.id)
                pullrequest.save()
                labels.remove(l)
    
    for label in labels:
        pullrequest.labels.add(label)
        pullrequest.save()
    
    return redirect('/pullrequest/updatePullrequestPage/'+ str(id))


def delete_labels_on_pull_request(request, id, label_id):
    pullrequest = get_object_or_404(Pullrequest, id=id)
    pullrequest.labels.remove(label_id)
    pullrequest.save()

    return redirect('/pullrequest/updatePullrequestPage/'+ str(id))

def add_milestones_on_pull_request(request, id):
    pullrequest = get_object_or_404(Pullrequest, id=id)
    milestones = request.POST.get('milestones')
   
    pullrequest.milestone.clear()
    milestone = get_object_or_404(Milestone, id=milestones)
    pullrequest.milestone.add(milestone)
    pullrequest.save()
        
    return redirect('/pullrequest/updatePullrequestPage/'+ str(id))


def add_issues_on_pull_request(request, id):
    pullrequest = get_object_or_404(Pullrequest, id=id)
    issues = request.POST.getlist('issues')

    for i in issues:
        issue = get_object_or_404(Issue, id=i)
        issue.pullrequests.add(pullrequest)
        issue.save()

    return redirect('/pullrequest/updatePullrequestPage/'+ str(id))

def get_connected_issues_to_pull_request(id, issues):
    connected_issues = list()

    for i in issues:
        for p in i.pullrequests.all():
            if p.id == id:
                connected_issues.append(i)
            
    return connected_issues

def delete_issues_on_pull_request(request, id, pr_id):
    issue = get_object_or_404(Issue, id=id)

    issue.pullrequests.remove(pr_id)
    issue.save()

    return redirect('/pullrequest/updatePullrequestPage/'+ str(pr_id))

def add_projects_in_pull_request(request, id):
    pullrequest = get_object_or_404(Pullrequest, id=id)
    projects = request.POST.getlist('projects')

    for project in projects:
        for p in pullrequest.projects.all():
            if project == p.id:
                pullrequest.assignees.remove(p.id)
                pullrequest.save()
                projects.remove(p)
    
    for project in projects:
        pullrequest.projects.add(project)
        pullrequest.save()

    return redirect('/pullrequest/updatePullrequestPage/'+ str(id))

def delete_projects_on_pull_request(request, id, project_id):
    pullrequest = get_object_or_404(Pullrequest, id=id)
    pullrequest.projects.remove(project_id)
    pullrequest.save()

    return redirect('/pullrequest/updatePullrequestPage/'+ str(id))
