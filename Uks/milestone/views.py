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

