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
from label.models import Label

from django.contrib import messages




@login_required(login_url="login")
def index(request, id):
    template = loader.get_template('repository/index.html')
    repository = Repository.objects.get(id=id)
    my_milestones, my_pullrequests, issues,branch_list,default_branch,commit_list,watchers,stargazers,forks,forked_from = get_repo_infos(request,id)
    show = ''
    if (forked_from != request.user): 
        show = 'Forked repo'

    return render(request, "repository/index.html", {
        'repository':repository,
        'milestones': my_milestones,
        'pullrequests': my_pullrequests,
        'issues': issues,
        'branch_list': branch_list,
        'commit_list': commit_list,
        'selected_branch': default_branch,
        'logged_user_id': request.user.id,
        'watchers':watchers,
        'stargazers': stargazers,
        'forks':forks,
        'forked_from': forked_from,
        'show':show})

def get_repo_infos(request,id):
    repository = Repository.objects.get(id=id)
    my_milestones = get_my_milestones(request,id)
    my_pullrequests = get_my_pullrequests(request, id)
    issues = get_issues_by_repo(request, id)
    branch_list = Branch.objects.all().filter(repository = id)
    default_branch = Branch.objects.all().filter(is_default = True, repository = repository)[0]  
    commit_list = Commit.objects.all().filter(branch = default_branch)
    print(commit_list)
    watchers = User.objects.all().filter(user_watchers = repository)
    stargazers = User.objects.all().filter(user_stargazers = repository)
    forks = User.objects.all().filter(user_forks = repository)
    #to do trebalo bi dodati kreiranje nekih labela 
    forkers,forked_from, forked_repo, repo_copy = find_forkers_info(request,id, repository)

    return my_milestones, my_pullrequests,issues,branch_list,default_branch,commit_list,watchers,stargazers,forks,forked_from

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
            newRepository.watchers.add(creator)
            add_initial_labels(newRepository)
            branch = Branch.objects.create(
                name = 'master',
                is_default = True,
                repository = Repository.objects.get(pk = newRepository.id)
            )  
    return redirect("all_repositories")

def add_initial_labels(newRepository):
    bug_label = Label(name = 'bug', description = "Something isn't working", color = '#ff2e1f', repository = newRepository)
    bug_label.save() 
    documentation_label = Label(name = 'documentation', description = "Improvements or additions to documentation", color = '#0073ff', repository = newRepository)
    documentation_label.save() 
    enhancment_label = Label(name = 'enhancment', description = "New feature or request", color = '#30feff', repository = newRepository)
    enhancment_label.save() 
    first_issue_label = Label(name = 'good first issue', description = "Good first issue", color = '#8974c5', repository = newRepository)
    first_issue_label.save() 
    help_wanted_label = Label(name = 'help wanted', description = "Extra attention is needed", color = '#ffee00', repository = newRepository)
    help_wanted_label.save() 
    question_label = Label(name = 'question', description = "Further information is requested", color = '#e816ff', repository = newRepository)
    question_label.save()
    invalid_label = Label(name = 'invalid', description = "This doesn't seem right", color = '#7efa19', repository = newRepository)
    invalid_label.save()  


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

    return render(request, 'repository/watchers.html',{"repository": repository,"watchers":watchers,"stargazers":stargazers,
        "forkers":forkers})

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

    return render(request, 'repository/stargazers.html',{"repository": repository,"stargazers":stargazers,"watchers": watchers,
        "forkers": forkers})

def forkRepository(request,id):
    repository = Repository.objects.get(id=id)
    repositories = Repository.objects.all().filter(creator=request.user)
    forks = User.objects.all().filter(user_forks = repository)
    user = User.objects.get(id=request.user.id) 
    if (repository.creator == user):
        message = 'You can not fork your own repository!'
        my_milestones, my_pullrequests, issues,branch_list,default_branch,commit_list,watchers,stargazers,forks,forked_from_user = get_repo_infos(request,id)
        return render(request, "repository/index.html", {'repository':repository,'milestones': my_milestones,'pullrequests': my_pullrequests,
        'issues': issues,'branch_list': branch_list,'commit_list': commit_list,'selected_branch': default_branch,'watchers':watchers,
        'stargazers': stargazers,'forks':forks,'forked_from': forked_from_user,'message':message})

    newRepository = None
    if request.user not in forks:
        newRepository = Repository(name = repository.name, status = repository.status, creator = request.user)
        newRepository.save()
        newRepository.developers.add(repository.creator)
        branch = Branch.objects.create(
                name = 'master',
                is_default = True,
                repository = Repository.objects.get(pk = newRepository.id)
            )  
        repository.forks.add(user)
        newRepository.forks.add(user)
    else:
        message = 'You have already forked this repo'
        my_milestones, my_pullrequests, issues,branch_list,default_branch,commit_list,watchers,stargazers,forks,forked_from_user = get_repo_infos(request,id)
        return render(request, "repository/index.html", {'repository':repository,'milestones': my_milestones,'pullrequests': my_pullrequests,
        'issues': issues,'branch_list': branch_list,'commit_list': commit_list,'selected_branch': default_branch,'watchers':watchers,
        'stargazers': stargazers,'forks':forks,'forked_from': forked_from_user,'message':message})

    return redirect('/repository/'+ str(newRepository.id))

def forkers(request,id):
    repository = Repository.objects.get(id=id)
    watchers = User.objects.all().filter(user_watchers = repository)
    stargazers = User.objects.all().filter(user_stargazers = repository)
    forkers,forked_from, forked_repo, repo_copy = find_forkers_info(request,id, repository)
    show = ''
    if (forked_from != request.user): 
        show = 'Forked repo'
    
    return render(request, 'repository/forkers.html',{"repository": repository,"watchers":watchers,"stargazers":stargazers,"forks": forkers,
        "forked_from":forked_from,"forked_repo":forked_repo,"repo_copy":repo_copy, "show":show})

def find_forkers_info(request,id,repository):
    forkers = User.objects.all().filter(user_forks = repository)
    forked_from = None
    forked_repo = None
    proba = None
    repo_copy = None
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
    
    return forkers, forked_from, forked_repo, repo_copy

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
    repository = Repository.objects.get(id = id)
    developer = User.objects.get(id = developer_id)
    developers = User.objects.all()
    collaborators = add_collaborator_on_repository(repository, developer)    
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
    return render(request,"repository/collaborators.html",{
         'repository':repository,
         'selected_developer': selected_developer,
         'collaborators': only_collaborators, 'developers':not_added_developers})

def add_collaborator_on_repository(repository, developer):
    repository.save()
    repository.developers.add(developer)
    collaborators = User.objects.all().filter(user_developers = repository)
    return collaborators

def remove_collaborator(request, id, developer_id):
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

def search_in_this_repo(request, id):
    if request.method == 'POST':
        repository = Repository.objects.get(id=id)
        searchedWord = request.POST['search']
        words = searchedWord.split()
        issues = checkIssues(words, repository)
        commits = checkCommits(words, repository)
        issuesIds=[]
        for issu in issues:
            issuesIds.append(issu.id)
        commitsIds=[]
        for c in commits:
            commitsIds.append(c.id)
        
    return render(request, 'repository/searchedRepoResult.html', {"foundCommits":commitsIds, 
    "commits":commits,"foundIssues":issuesIds, "issues":issues,
    "repository":repository, 
    "searchedWords":searchedWord})


def checkIssues(words, repository):
    issues = []
    all_repo_issues = Issue.objects.all().filter(repository = repository)
    for issue in all_repo_issues:
            for word in words:
                if (word.lower() in issue.issue_title.lower() or word.lower() in issue.description.lower() ):
                    if (len(issues) == 0):
                        issues.append(issue)
                    elif(issue not in issues):
                        issues.append(issue)
    return issues

def checkCommits(words, repository):
    commits = [] 
    branch_list = Branch.objects.all().filter(repository = repository)
    all_commits = Commit.objects.all()
    for branch in branch_list:
        for commit in all_commits:
            if (branch.id == commit.branch.id):
                for word in words:
                    if (word.lower() in commit.message.lower()):
                        if (len(commits) == 0):
                            commits.append(commit)
                        elif(commit not in commits):
                            commits.append(commit)
    return commits

def searched_repo_issues(request, id):
    if request.method == 'POST':
      repository, issues, issuesIds, commits, commitsIds,searchedWords = find_all_searched_items(request,id)
    return render(request, 'repository/searchedRepoIssues.html',{"foundCommits":commitsIds, 
    "commits":commits,"foundIssues":issuesIds, "issues":issues, "repository": repository,
    "searchedWords":searchedWords})

def searched_repo_commits(request, id):
    if request.method == 'POST':
       repository, issues, issuesIds, commits, commitsIds,searchedWords = find_all_searched_items(request,id)
    return render(request, 'repository/searchedRepoCommits.html',{"foundCommits":commitsIds, 
    "commits":commits,"foundIssues":issuesIds, "issues":issues, "repository":repository,
    "searchedWords":searchedWords})

def findIssues(request):
    foundIssues = request.POST.get('foundIssues')
    issues = []
    if (foundIssues != '[]'):
        issuesFound = foundIssues.strip('][').split(', ')
        for foundIssue in issuesFound:
            issue = get_object_or_404(Issue, id = foundIssue)
            issues.append(issue)
    return issues

def findIssuesIds(request):
    issues = findIssues(request)
    issuesIds=[]
    for issu in issues:
        issuesIds.append(issu.id)
    return issuesIds

def findCommits(request):
    foundCommits = request.POST.get('foundCommits')
    commits = []
    if (foundCommits != '[]'):
        commitsFound = foundCommits.strip('][').split(', ')
        for foundCommit in commitsFound:
            commit = get_object_or_404(Commit, id = foundCommit)
            commits.append(commit)
    return commits

def findCommitsIds(request):
    commits = findCommits(request)
    commitsIds=[]
    for c in commits:
        commitsIds.append(c.id)
    return commitsIds

def find_all_searched_items(request,id):
    repository = Repository.objects.get(id=id)
    issues = findIssues(request)
    issuesIds = findIssuesIds(request)
    commits = findCommits(request)
    commitsIds = findCommitsIds(request)
    searchedWords = request.POST.get('searchedWords')

    return repository, issues, issuesIds, commits, commitsIds,searchedWords
