from django.shortcuts import render, get_object_or_404, redirect
from .models import Milestone
from repository.models import Repository

def newMilestone(request, id):
    return render(request, 'newMilestone.html', {"repository_id":id})

def milestones(request,id):
    milestones = Milestone.objects.all()
    repositoryMilestones=[]
    for m in milestones:
        if(m.repository.id == id):
            repositoryMilestones.append(m)
    return repositoryMilestones
    #return render(request, 'milestones.html', {"milestones":repositoryMilestones})

def deleteMilestone(request, id):
    milestone = get_object_or_404(Milestone, id=id)
    all_repos = Repository.objects.all()
    for r in all_repos:
        if(r.id == milestone.repository.id):
            repository = r
    milestone.delete()
    milestonesUpdated = milestones(request, repository.id)
    return render(request, "milestones.html", {"milestones":milestonesUpdated, "repository_id":repository.id})

def addMilestone(request):
    errorTitle = None
    if request.method == 'POST':
        title = request.POST['title']
        dueDate = request.POST['dueDate']
        description = request.POST['description']
        repository = get_object_or_404(Repository, id = request.POST['repository_id'] )
        if title is not None and title == "":
            errorTitle = "Please enter title!"
            return render(request, "newMilestone.html", {"errorTitle": errorTitle})
        else:
            if dueDate=="":
                newMilestone = Milestone(title = title, description = description, repository = repository)
            else:
                newMilestone = Milestone(title = title, due_date = dueDate, description = description, repository = repository)
            newMilestone.save()
            newMilestones = milestones(request, repository.id)
    #return redirect('milestones')
    return render(request, "milestones.html", {"milestones":newMilestones, "repository_id": repository.id})

def getMilestoneById(request, id):
    milestone = get_object_or_404(Milestone, id = id)
    return render(request, "updateMilestone.html", {"milestone": milestone})

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
        milestonesUpdated = milestones(request, repository.id)
        return render(request, "milestones.html", {"milestones":milestonesUpdated, "repository_id":repository.id})
        #return redirect('milestones')