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
    print(commit_list)
    return render(request, "repository/index.html", {
        'repository':repository,
        'milestones': my_milestones,
        'pullrequests': my_pullrequests,
        'issues': issues,
        'branch_list': branch_list,
        'commit_list': commit_list,
        'selected_branch': default_branch,
        'logged_user_id': request.user.id})

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
            messages.success(request, 'Repository has been created.')
            newRepository.developers.add(creator)
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
    messages.success(request, 'Repository has been updated.')
    return redirect("/repository/all_repositories")

def deleteRepository(request,id):
    repo = Repository.objects.get(id=id)
    pullrequests = Pullrequest.objects.all()
    for pr in pullrequests:
        if pr.prRepository == repo:
            pr.prRepository = None
    
    repo.delete()
    messages.success(request, 'Repository has been deleted.')
    return redirect("/repository/all_repositories")

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

def collaborators(request, id):
    repository = Repository.objects.get(id = id)
    collaborators = User.objects.all().filter(user_developers = repository)
    only_collaborators = []
    for collab in collaborators:
        if collab.id != repository.creator.id:
            only_collaborators.append(collab)
    developers = User.objects.all()
    not_added_developers = []
    for developer in developers:
        if developer not in collaborators and developer.id != repository.creator.id:
            not_added_developers.append(developer)
    selected_developer = User.objects.first()
    return render(request, "repository/collaborators.html",{'repository':repository, 'collaborators':only_collaborators,'selected_developer': selected_developer, 'developers':not_added_developers, 'logged_user_id': request.user.id})

def repo_developer(request, id, developer_id):
    print("repo developer")
    print(developer_id)
    template = loader.get_template('repository/collaborators.html')
    repository = Repository.objects.get(id=id)
    developers = User.objects.all()
    developers_without_creator = filter(lambda id: id != repository.creator.id, developers)
    collaborators = User.objects.all().filter(user_developers = repository)
    only_collaborators = []
    for collab in collaborators:
        if collab.id != repository.creator.id:
            only_collaborators.append(collab)
    not_added_developers = []
    for developer in developers:
        if developer not in collaborators and developer.id != repository.creator.id:
            not_added_developers.append(developer)
    selected_developer = get_object_or_404(User, id = developer_id)
    return render(request, "repository/collaborators.html", {
        'repository':repository,
        'selected_developer': selected_developer,
        'collaborators':only_collaborators, 'developers':not_added_developers})

def add_collaborator(request, id, developer_id):
    print(developer_id)
    repository = Repository.objects.get(id = id)
    developer = User.objects.get(id = developer_id)
    developers = User.objects.all()
    collaborators =add_collaborator_on_repository(repository, developer)    
    only_collaborators = []
    for collab in collaborators:
        if collab.id != repository.creator.id:
            only_collaborators.append(collab)
    not_added_developers = []
    for developer in developers:
        if developer not in collaborators and developer.id != repository.creator.id:
            not_added_developers.append(developer)
    if len(not_added_developers)>0 :
        selected_developer = not_added_developers[0]
    else:
        selected_developer = User.objects.first()
    print('id narednog posle dodavanja je ')
    print(selected_developer)
    return render(request,"repository/collaborators.html",{
         'repository':repository,
         'selected_developer': selected_developer,
         'collaborators': only_collaborators, 'developers':not_added_developers})

def add_collaborator_on_repository(repository, developer):
    repository.developers.add(developer)
    collaborators = User.objects.all().filter(user_developers = repository)
    return collaborators

def remove_collaborator(request, id, developer_id):
    print(developer_id)
    repository = Repository.objects.get(id = id)
    developer = User.objects.get(id = developer_id)
    remove_collaborato_from_repository(repository, developer)
    collaborators = User.objects.all().filter(user_developers = repository)
    only_collaborators = []
    for collab in collaborators:
        if collab.id != repository.creator.id:
            only_collaborators.append(collab)
    
    
    not_added_developers = []
    developers = User.objects.all()
    for developer in developers:
        if developer not in collaborators and developer.id != repository.creator.id:
            not_added_developers.append(developer)
    selected_developer = get_object_or_404(User, id = developer_id)
    return render(request, "repository/collaborators.html", { 'repository':repository,
         'selected_developer': selected_developer,
         'collaborators': only_collaborators, 'developers':not_added_developers})

def remove_collaborato_from_repository(repository, developer):
    repository.developers.remove(developer)
    collaborators = User.objects.all().filter(user_developers = repository)
    return collaborators