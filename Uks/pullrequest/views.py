from random import choices
from xml.etree.ElementTree import Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from repository.views import collaborators
from .models import MERGED, PULL_REQUEST_STATE, Pullrequest, Repository, Branch
from comment.models import EMOJI_PICKER
from datetime import date

def pullrequests(request, id):
    repository = get_object_or_404(Repository, id=id)
    pullrequests = Pullrequest.objects.all().filter(prRepository=repository)
    my_pullrequests = []
    for pr in pullrequests:
        if pr.creator == request.user:
            my_pullrequests.append(pr)
    print("broj pulrequestova je ")
    print(pullrequests)
    pullrequests_for_review = get_pullrequests_for_review(request, repository)
    return render(request, 'pullrequests.html', {"pullrequests":my_pullrequests, "repository":repository,'pullrequests_for_review':pullrequests_for_review})

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
    return render(request, 'newPullrequest.html', {"branches":branches, "repository":repository})

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
        return render(request, "updatePullrequest.html", {'reviewers': reviewers, 'not_assigned_collaborators_on_repository': not_assigned_collaborators_on_repository,"pullrequest": newPullrequest, "repository": prRepository})

def updatePullrequestPage(request, id):
    pullrequest, repository, comments, emojis, not_assigned_collaborators_on_repository, reviewers = pull_request_page_data(request, id)
    return render(request, "updatePullrequest.html", {'reviewers': reviewers, 'not_assigned_collaborators_on_repository': not_assigned_collaborators_on_repository,"pullrequest": pullrequest, "repository": repository, "comments":comments, "emojis":emojis})

def get_not_assigned_collaborators_on_pull_request(request,reviewers,prRepository):
    collaborators_on_repository = User.objects.all().filter(user_developers = prRepository).all()
    print("collaborators_on_repository")
    print(len(collaborators_on_repository))
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
    return pullrequest, repository, comments, emojis, not_assigned_collaborators_on_repository, reviewers

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
    pullrequest, repository, comments, emojis, not_assigned_collaborators_on_repository, reviewers=pull_request_page_data(request, pullrequest_id)
    return render(request, "updatePullrequest.html", {'reviewers': reviewers, 'not_assigned_collaborators_on_repository': not_assigned_collaborators_on_repository, "pullrequest": pullrequest, "repository": repository, "comments":comments, "emojis":emojis})

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
    print(len(pullrequest.reviewers.all()))
    if len(pullrequest.reviewers.all()) == 0 and pullrequest.reviewed:
        pullrequest.status = "Merged"
        pullrequest.save()
    pullrequests = Pullrequest.objects.all().filter(prRepository=repository)
    my_pullrequests = []
    for pr in pullrequests:
        if pr.creator == request.user:
            my_pullrequests.append(pr)
    pullrequests_for_review = get_pullrequests_for_review(request, repository)
    return render(request, 'pullrequests.html', {"pullrequests":my_pullrequests, "repository":repository,'pullrequests_for_review':pullrequests_for_review})
