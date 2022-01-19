from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from home.views import repository
from .models import Repository
from milestone.models import Milestone

# Create your views here.

@login_required(login_url="login")
def index(request, id):
    template = loader.get_template('repository/index.html')
    repository = Repository.objects.get(id=id)
    my_milestones = get_my_milestones(request,id)
    return render(request, "repository/index.html", {'repository':repository ,'milestones': my_milestones})

def get_my_milestones(request, id):
    milestones = Milestone.objects.all()
    repositoryMilestones=[]
    for m in milestones:
        if(m.repository.id == id):
            repositoryMilestones.append(m)
    return repositoryMilestones
