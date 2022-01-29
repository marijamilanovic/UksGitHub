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
    stargazers = User.objects.all().filter(user_stargazers = repository)
    forks = User.objects.all().filter(user_forks = repository)
    #to do trebalo bi dodati kreiranje nekih labela 
    
    repositories_with_same_name = Repository.objects.all().filter(name = repository.name)
    forked_from_user = None
    for r in repositories_with_same_name:
        if (r.creator.id != repository.creator.id):
            forked_from_user = get_object_or_404(User, id=r.creator.id)
    print(forked_from_user)
    
    
    return render(request, "repository/index.html", {
        'repository':repository,
        'milestones': my_milestones,
        'pullrequests': my_pullrequests,
        'issues': issues,
        'branch_list': branch_list,
        'commit_list': commit_list,
        'selected_branch': default_branch,
        'watchers':watchers,
        'stargazers': stargazers,
        'forks':forks,
        'forked_from': forked_from_user})

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
    watchers = User.objects.all().filter(user_watchers = repository)
    user = User.objects.get(id=request.user.id)
    if request.user not in watchers:
        repository.watchers.add(user)
    else:
        repository.watchers.remove(user)
    
    return redirect('/repository/'+ str(repository.id))

def watchers(request,id):
    repository = Repository.objects.get(id=id)
    watchers = User.objects.all().filter(user_watchers = repository)
    stargazers = User.objects.all().filter(user_stargazers = repository)
    forkers = User.objects.all().filter(user_forks = repository)
    return render(request, 'repository/watchers.html',{
        "repository": repository,
        "watchers":watchers,
        "stargazers":stargazers,
        "forkers":forkers
    })

def starRepository(request,id):
    repository = Repository.objects.get(id=id)
    stargazers = User.objects.all().filter(user_stargazers = repository)
    user = User.objects.get(id=request.user.id)
    if (user not in stargazers):
        repository.stargazers.add(user)
    else:  
        repository.stargazers.remove(user)
    return redirect('/repository/'+ str(repository.id))

def stargazers(request,id):
    repository = Repository.objects.get(id=id)
    stargazers = User.objects.all().filter(user_stargazers = repository)
    watchers = User.objects.all().filter(user_watchers = repository)
    forkers = User.objects.all().filter(user_forks = repository)
    return render(request, 'repository/stargazers.html',{
        "repository": repository,
        "stargazers":stargazers,
        "watchers": watchers,
        "forkers": forkers
    })

def forkRepository(request,id):
    repository = Repository.objects.get(id=id)
    repositories = Repository.objects.all().filter(creator=request.user)
    newRepository = Repository(name = repository.name, status = repository.status, creator = request.user)
    newRepository.save()
    newRepository.developers.add(repository.creator)
    branch = Branch.objects.create(
                name = 'master',
                is_default = True,
                repository = Repository.objects.get(pk = newRepository.id)
            )  
    forks = User.objects.all().filter(user_forks = newRepository)
    user = User.objects.get(id=request.user.id)
    if request.user not in forks:
        repository.forks.add(user)
        newRepository.forks.add(user)
    else:
        repository.forks.remove(user)
        newRepository.forks.add(user)

    return redirect('/repository/'+ str(newRepository.id))

def forkers(request,id):
    repository = Repository.objects.get(id=id)
    watchers = User.objects.all().filter(user_watchers = repository)
    stargazers = User.objects.all().filter(user_stargazers = repository)
    forkers = User.objects.all().filter(user_forks = repository)
    forked_from = None
    forked_repo = None
    proba = None
    for f in forkers:
        if (f.id == repository.creator.id):  
            repo = Repository.objects.get(id=repository.id)  
            repos_with_same_name = Repository.objects.all().filter(name = repo)
            for r in repos_with_same_name:
                if (r.creator.id != repo.creator.id):
                    forked_from = get_object_or_404(User, id=r.creator.id)
                    forked_repo = r
                    repo_copy = repo
                    break
                else:
                    forked_from = get_object_or_404(User, id=r.creator.id)
            
        else:
            repo = Repository.objects.get(id = repository.id)  
            repos_with_same_name = Repository.objects.all().filter(name = repo)
            if (f.id != repo.creator.id):
                repos = Repository.objects.all().filter(creator = f, name = repo.name) 
                repo_copy = repos[0]
            
            for r in repos_with_same_name:
                if (r.creator.id != repo.creator.id): 
                    forked_from = get_object_or_404(User, id=r.creator.id)
                    forked_repo = r  
                else:
                    forked_from = get_object_or_404(User, id=repo.creator.id)
                    forked_repo = repo
                    break
    
    return render(request, 'repository/forkers.html',{
        "repository": repository,
        "watchers":watchers,
        "stargazers":stargazers,
        "forks": forkers,
        "forked_from":forked_from,
        "forked_repo":forked_repo,
        "repo_copy":repo_copy
    })

