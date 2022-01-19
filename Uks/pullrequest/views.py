from django.shortcuts import render, get_object_or_404, redirect
from .models import Pullrequest, Repository, Branch
from datetime import date

def pullrequests(request, id):
    repository = get_object_or_404(Repository, id=id)
    pullrequests = Pullrequest.objects.all().filter(prRepository=repository)
    return render(request, 'pullrequests.html', {"pullrequests":pullrequests, "repository":repository})


def newPullrequest(request, id):
    repository = get_object_or_404(Repository, id=id)
    branches = Branch.objects.all().filter(repository=repository)
    return render(request, 'newPullrequest.html', {"branches":branches, "repository":repository})

def addPullrequest(request):
    if request.method == 'POST':
        created = date.today()
        prRepository = get_object_or_404(Repository, id = request.POST['repository'] )
        print(request.POST['branch_source_id'])
        source = get_object_or_404(Branch, id = request.POST['branch_source_id'] )
        target = get_object_or_404(Branch, id = request.POST['branch_target_id'] )
        name = target.name

        newPullrequest = Pullrequest(name = name, status = 'Opened', created = created, prRepository = prRepository, source = source, target = target)
        newPullrequest.save()
        newPullrequests = pullrequests(request, prRepository.id)
    
    return redirect('/pullrequest/pullrequests/'+str(prRepository.id))
