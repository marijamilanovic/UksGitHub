from django.shortcuts import render, get_object_or_404, redirect
from .models import Milestone

# Create your views here.
def newMilestone(request):
    return render(request, 'newMilestone.html', {})

def milestones(request):
    milestones = Milestone.objects.all()
    return render(request, 'milestones.html', {"milestones":milestones})

def deleteMilestone(request, id):
    milestone = get_object_or_404(Milestone, id=id)
    milestone.delete()
    return redirect('milestones')

def addMilestone(request):
    errorTitle = None
    if request.method == 'POST':
        title = request.POST['title']
        dueDate = request.POST['dueDate']
        description = request.POST['description']
        if title is not None and title == "":
            errorTitle = "Please enter title!"
            return render(request, "newMilestone.html", {"errorTitle": errorTitle})
        else:
            if dueDate=="":
                newMilestone = Milestone(title = title, description = description)
            else:
                newMilestone = Milestone(title = title, due_date = dueDate, description = description)
            newMilestone.save()
    return redirect('milestones')

def getMilestoneById(request, id):
    milestone = get_object_or_404(Milestone, id = id)
    return render(request, "updateMilestone.html", {"milestone": milestone})

def updateMilestone(request, id):
    if request.method == 'POST':
        milestone = get_object_or_404(Milestone, id = id)
        milestone.title = request.POST['title']
        milestone.due_date = request.POST['dueDate']
        milestone.description = request.POST['description']
        milestone.save()
        return redirect('milestones')
