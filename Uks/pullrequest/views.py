from django.shortcuts import render, get_object_or_404, redirect
from .models import Pullrequest, Repository, Branch

#def getActivePRs(request, id):


def openedPRs(request):
    if request.method=='GET':
        repository = get_object_or_404(Repository, id=1)
        openedPRs = Pullrequest.objects.all().filter(prRepository=repository, status = 'Opened')
        return render(request, 'pullrequests.html', {"openedPRs":openedPRs})

def closedPRs(request):
    if request.method=='GET':
        repository = get_object_or_404(Repository, id=1)
        closedPRs = Pullrequest.objects.all().filter(prRepository=repository, status = 'Closed')
        return render(request, 'pullrequests.html', {"closedPRs":closedPRs})

