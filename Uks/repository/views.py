from django.shortcuts import render
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
    #ovde dobavis sve za izabrani repo
    my_milestones = get_my_milestones(request)  #trenutno sve dok model ne povezes
    return render(request, "repository/index.html", {'repository':repository ,'milestones': my_milestones})

def get_my_milestones(request):
    return Milestone.objects.all()