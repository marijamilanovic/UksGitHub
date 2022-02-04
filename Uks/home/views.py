from getpass import getuser
import re
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Uks.decorators import authorized
from repository.models import Repository
from user.models import User
from milestone.models import Milestone
from issue.models import Issue
from django.db.models import Q

# Create your views here.


@login_required(login_url="login")
def index(request):
    template = loader.get_template('home/index.html')
    my_repositories = get_my_repos(request)
    all_repositories = my_repositories
    # add other repositories
    return render(request, "home/index.html", {'all_repositories':all_repositories})

@login_required(login_url="login")
def profile(request):
    template = loader.get_template('home/profile.html')
    my_repositories = get_my_repos(request)
    my_milestones = get_my_milestones(request)
    #my_issues = get_my_issues(request)
    all_users = get_all_users()
    return render(request, "home/profile.html", {
        'my_repositories': my_repositories, 
        'milestones': my_milestones,
        'all_users':all_users})

def get_all_users():
    return User.objects.all()

def repository(request, id):
    return redirect('/repository/' + id)

# def editRepository(request, id):
#     return redirect('/editRepository/' + id)

# def deleteRepository(request, id):
#     return redirect('/deleteRepository/' + id)
def get_my_repos(request):
    repos_creator = Repository.objects.filter(Q(creator_id = request.user.id))
    repos_collaborators = Repository.objects.filter(Q(developers=request.user))
    if repos_collaborators:
        repos_collaborators.union(repos_creator)
        return repos_collaborators
    return repos_creator

def get_my_milestones(request):
    return Milestone.objects.all()

def can_user_access_private_repo(request, repository):
    if request.user.id == repository.creator_id or Repository.objects.filter(developers=request.user.id).exists():
        print(Repository.objects.filter(developers=request.user.id))
        return True
    else:
        return False

