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
    my_issues = get_my_issues(request)
    all_users = get_all_users()
    return render(request, "home/profile.html", {
        'my_repositories': my_repositories, 
        'milestones': my_milestones,
        'my_issues': my_issues,
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
    return Repository.objects.filter(creator_id=request.user.id)

def get_my_milestones(request):
    return Milestone.objects.all()

def get_my_issues(request):
    issues = Issue.objects.filter(opened_by=request.user.username)
    issues = issues.union(Issue.objects.filter(assignee=request.user.username))
    return issues
