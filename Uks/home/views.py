from getpass import getuser
import re
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from Uks.decorators import authorized
from repository.models import Repository
from user.models import User

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
    return render(request, "home/profile.html", {'my_repositories': my_repositories})


def repository(request, id):
    return redirect('/repository/' + id)

def get_my_repos(request):
    return Repository.objects.filter(creator_id=request.user.id)