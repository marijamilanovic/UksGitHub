from random import choices
from xml.etree.ElementTree import Comment
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pullrequest, Repository, Branch
from comment.models import EMOJI_PICKER
from datetime import date

def pullrequests(request, id):
    repository = get_object_or_404(Repository, id=id)
    pullrequests = Pullrequest.objects.all().filter(prRepository=repository)
    return render(request, 'pullrequests.html', {"pullrequests":pullrequests, "repository":repository, "logged_user_id":request.user.id})


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
        newPullrequest.save()
    
        return render(request, "updatePullrequest.html", {"pullrequest": newPullrequest, "repository": prRepository})

def updatePullrequestPage(request, id):
    pullrequest = get_object_or_404(Pullrequest, id = id)
    repository = get_object_or_404(Repository, id = pullrequest.prRepository.id)
    comments = pullrequest.comments.all()
    emojis = list()
    for e in EMOJI_PICKER:
        emojis.append(e[0])
    return render(request, "updatePullrequest.html", {"pullrequest": pullrequest, "repository": repository, "comments":comments, "emojis":emojis})


def changeStatusPullrequest(request, id):
    pullrequest = get_object_or_404(Pullrequest, id = id)
    if(pullrequest.status=='Closed'):
        pullrequest.status = 'Opened'
    elif(pullrequest.status=='Opened'):
        pullrequest.status = 'Closed'
    pullrequest.save()
    return redirect('/pullrequest/pullrequests/'+str(pullrequest.prRepository.id))

