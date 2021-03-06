from django.shortcuts import render, get_object_or_404, redirect
from .models import Milestone
from repository.models import Repository
from issue.models import Issue
from datetime import date
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url="login")
def newMilestone(request, id):
    repository = get_object_or_404(Repository, id=id)
    return render(request, 'newMilestone.html', { "repository":repository, "logged_user_id": request.user.id})

def milestones(request,id):
    milestones = Milestone.objects.all()
    repositoryMilestones=[]
    for m in milestones:
        if(m.repository.id == id):
            repositoryMilestones.append(m)
    repository = get_object_or_404(Repository, id=id)
    
    return render(request, 'milestones.html', {"milestones":repositoryMilestones, "repository":repository, "logged_user_id": request.user.id})

def allMilestones(request):
    milestones = Milestone.objects.all()
    return render(request, 'milestones.html', {"milestones":milestones})

@login_required(login_url="login")
def deleteMilestone(request, id):
    milestone = get_object_or_404(Milestone, id=id)
    if not milestone.repository.developers.all().filter(id=request.user.id):
        return HttpResponse('401 Unauthorized', status=401)
    all_repos = Repository.objects.all()
    for r in all_repos:
        if(r.id == milestone.repository.id):
            repository = r
    milestone.delete()
    milestonesUpdated = Milestone.objects.all().filter(repository=milestone.repository)
    messages.success(request, 'Milestone has been deleted.')
    return redirect('/milestone/milestones/'+ str(repository.id))

@login_required(login_url="login")
def addMilestone(request):
    errorTitle = None
    if request.method == 'POST':
        title = request.POST['title']
        dueDate = request.POST['dueDate']
        description = request.POST['description']
        repository = get_object_or_404(Repository, id = request.POST['repository'] )
        if title is not None and title == "":
            errorTitle = "Please enter title!"
            return render(request, "newMilestone.html", {"errorTitle": errorTitle, "repository":repository})
        else:
            if dueDate=="":
                newMilestone = Milestone(title = title, description = description, repository = repository)
            else:
                newMilestone = Milestone(title = title, due_date = dueDate, description = description, repository = repository)
            newMilestone.save()
            messages.success(request, 'Milestone has been created.')
    return redirect('/milestone/milestones/'+ str(repository.id))

def getMilestoneById(request, id):
    milestone = get_object_or_404(Milestone, id = id)
    repository = get_object_or_404(Repository, id = milestone.repository.id)

    return render(request, "updateMilestone.html", {"milestone": milestone, "repository": repository})

@login_required(login_url="login")
def updateMilestone(request, id):
    if request.method == 'POST':
        milestone = get_object_or_404(Milestone, id = id)
        milestone.title = request.POST['title']
        milestone.due_date = request.POST['dueDate']
        milestone.description = request.POST['description']
        all_repos = Repository.objects.all()
        for r in all_repos:
            if(r.id == milestone.repository.id):
                repository = r
        milestone.save()
        messages.success(request, 'Milestone has been updated.')
    return redirect('/milestone/milestones/'+ str(repository.id))

def seeMilestone(request, id):
    milestone = get_object_or_404(Milestone, id = id)
    repository = get_object_or_404(Repository, id = milestone.repository.id)
    issues = Issue.objects.all().filter(milestone=milestone.id)

    return render(request, "milestone.html", {"milestone": milestone, "repository": repository, "issues":issues })

@login_required(login_url="login")
def closeMilestone(request,id):
    milestone = get_object_or_404(Milestone, id = id)
    milestone.status = 'Closed'
    milestone.save()
    return redirect('/milestone/milestones/'+ str(milestone.repository.id))

@login_required(login_url="login")
def reopenMilestone(request,id):
    milestone = get_object_or_404(Milestone, id = id)
    milestone.status = 'Opened'
    milestone.save()
    return redirect('/milestone/milestones/'+ str(milestone.repository.id))