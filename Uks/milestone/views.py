from django.shortcuts import render
from .models import Milestone

# Create your views here.
def newMilestone(request):
    return render(request, 'newMilestone.html', {})

def milestones(request):
    milestones = Milestone.objects.all()
    return render(request, 'milestones.html', {"milestones":milestones})

