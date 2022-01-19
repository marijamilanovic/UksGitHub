from django.shortcuts import render, get_object_or_404, redirect
from .models import Pullrequest, Repository, Branch
import datetime

def pullrequests(request, id):
    repository = get_object_or_404(Repository, id=id)
    pullrequests = Pullrequest.objects.all().filter(prRepository=repository)
    return render(request, 'pullrequests.html', {"pullrequests":pullrequests, "repository":repository})


def newPullrequest(request, id):
    return render(request, 'newPullrequest.html', {"repository_id":id})

def addPullrequest(request):
    if request.method == 'POST':
        name = request.POST['name']
        created = datetime.now()
        prRepository = get_object_or_404(Repository, id = request.POST['repository_id'] )
        source = get_object_or_404(Branch, id = request.POST['branch_source_id'] )
        target = get_object_or_404(Branch, id = request.POST['branch_target_id'] )
        comments = request.POST['comment']

        if title is not None and title == "":
            errorTitle = "Please enter title!"
            return render(request, "newPullrequest.html", {"errorTitle": errorTitle})
        else:
            newPullrequest = Pullrequest(name = name, status = status, created = created, prRepository = prRepository, source = source, target = target)
            newPullrequest.save()
            newPullrequest = pullrequests(request, repository.id)
    
    return render(request, "pullrequests.html", {"pullrequests":newPullrequest, "prRepository": repository.id})
