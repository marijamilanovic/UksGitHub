from django.shortcuts import render

# Create your views here.
def newMilestone(request):
    return render(request, 'newMilestone.html', {})

def milestones(request):
    return render(request, 'milestones.html', {})