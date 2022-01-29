from unicodedata import name
from xml.etree.ElementTree import Comment
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from user.models import UserAccount
from home.views import repository
from .models import Repository
from django.contrib.auth.models import User
from pullrequest.models import Pullrequest
from milestone.models import Milestone
from issue.models import Issue
from branch.models import Branch
from commit.models import Commit
from django.contrib import messages


@login_required(login_url="login")
def index(request, id):
    template = loader.get_template('repository/index.html')
    repository = Repository.objects.get(id=id)
    my_milestones = get_my_milestones(request,id)
    my_pullrequests = get_my_pullrequests(request, id)
    issues = get_issues_by_repo(request, id)
    branch_list = Branch.objects.all().filter(repository = id)
    default_branch = Branch.objects.all().filter(is_default = True, repository = repository)[0]
    commit_list = Commit.objects.all().filter(branch = default_branch)
    watchers = User.objects.all().filter(user_watchers = repository)
    #to do trebalo bi dodati kreiranje nekih labela 
    
    return render(request, "repository/index.html", {
        'repository':repository,
        'milestones': my_milestones,
        'pullrequests': my_pullrequests,
        'issues': issues,
        'branch_list': branch_list,
        'commit_list': commit_list,
        'selected_branch': default_branch,
        'watchers':watchers})

def get_my_milestones(request, id):
    milestones = Milestone.objects.all()
    repositoryMilestones=[]
    for m in milestones:
        if(m.repository.id == id):
            repositoryMilestones.append(m)
    return repositoryMilestones

def get_my_pullrequests(request, id):
    repository = get_object_or_404(Repository, id=id)
    pullrequests = Pullrequest.objects.all().filter(prRepository=repository)
    return pullrequests

def get_issues_by_repo(request, id):
    repository = get_object_or_404(Repository, id=id)
    issues = Issue.objects.filter(repository = repository)
    return issues

def newRepository(request):
    return render(request, "repository/newRepository.html")

def addRepository(request):
    errorTitle = None
    if request.method == 'POST':
        name = request.POST['name']
        status = request.POST['status']
        creator = request.user
        if name is not None and name == "":
            errorTitle = "Please enter name!"
            return render(request, "repository/newRepository.html", {"errorTitle": errorTitle})
        else:
            newRepository = Repository(name = name, status = status, creator = creator)
            newRepository.save()
            newRepository.developers.add(creator)
            newRepository.watchers.add(creator)
            branch = Branch.objects.create(
                name = 'master',
                is_default = True,
                repository = Repository.objects.get(pk = newRepository.id)
            )  
    return redirect("all_repositories")

def transferToEditRepository(request,id):
    repo = Repository.objects.get(id = id)
    return render(request, "repository/editRepository.html", {'repository':repo})

def editRepository(request):
    id = request.POST['id']
    name = request.POST['name']
    status = request.POST['status']
    repo = Repository.objects.get(id = id)
    repo.name = name
    repo.status = status
    repo.save()
    return redirect("../../home/")

def deleteRepository(request,id):
    repo = Repository.objects.get(id=id)
    pullrequests = Pullrequest.objects.all()
    for pr in pullrequests:
        if pr.prRepository == repo:
            pr.prRepository = None
    
    repo.delete()
    return redirect("../../home/")

def get_my_pullrequests(request, id):
    repository = get_object_or_404(Repository, id=id)
    pullrequests = Pullrequest.objects.all().filter(prRepository=repository)
    return pullrequests

def all_repositories(request):
    #prikazuju se samo koje je kreirao
    #koristi se na profilnoj stranici
    #treba obratiti paznju i na one gde je on developer
    all_repositories = Repository.objects.all().filter(creator = request.user)
    return render(request, 'repository/all_repositories.html',{'all_repositories':all_repositories})


def repo_branch(request, id, branch_id):
    template = loader.get_template('repository/index.html')
    repository = Repository.objects.get(id=id)
    my_milestones = get_my_milestones(request,id)
    my_pullrequests = get_my_pullrequests(request, id)
    issues = get_issues_by_repo(request, id)
    branch_list = Branch.objects.all().filter(repository = id)
    branch = get_object_or_404(Branch, id = branch_id)
    commit_list = Commit.objects.all().filter(branch = branch)
    print(commit_list)
    return render(request, "repository/index.html", {
        'repository':repository,
        'milestones': my_milestones,
        'pullrequests': my_pullrequests,
        'issues': issues,
        'branch_list': branch_list,
        'commit_list': commit_list,
        'selected_branch': branch,})

def watchRepository(request,id):
    repository = Repository.objects.get(id=id)
    print('************************')
    message = None
    watchers = User.objects.all().filter(user_watchers = repository)
    # ako user vec nije u toj listi dodaj ga
    print(request.user)
    user = User.objects.get(id=request.user.id)
    print(user)
    if request.user not in watchers:
        repository.watchers.add(user)
    else:
        #message = 'You are already watching! Do you want to unwatch this repository'
        repository.watchers.remove(user)
    return redirect('/repository/'+ str(repository.id))

def watchers(request,id):
    repository = Repository.objects.get(id=id)
    watchers = User.objects.all().filter(user_watchers = repository)
    return render(request, 'repository/watchers.html',{
        "repository": repository,
        "watchers":watchers
    })