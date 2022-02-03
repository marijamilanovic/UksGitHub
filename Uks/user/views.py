from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from repository.models import Repository
from issue.models import Issue
from commit.models import Commit
from branch.models import Branch
from project.models import Project
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html', {})

def loginUser(request):
    ok_login = False

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            ok_login = True
            return redirect('/home/')
        else:
            ok_login = False
            messages.info(request, "Invalid username or password")

    context = {'ok_login': ok_login}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    return redirect('/home/')

def profile(request):
    return redirect('/home/profile')

def search(request):
    if request.method == 'POST':
        searchedWord = request.POST['search']
        words = searchedWord.split()
        repositories = checkRepositories(words, request)
        issues = checkIssues(words)
        commits = checkCommits(words)
        #to do add users search
        users = checkUsers(words)
        issuesIds=[]
        for issu in issues:
            issuesIds.append(issu.id)
        commitsIds=[]
        for c in commits:
            commitsIds.append(c.id)
        repositoriesIds =[]
        for r in repositories:
            repositoriesIds.append(r.id)
        usersIds =[]
        for u in users:
            usersIds.append(u.id)

    return render(request, 'searchResult.html', {"foundCommits":commitsIds, 
    "commits":commits,"foundIssues":issuesIds, "issues":issues,
    "repositories":repositories, "foundRepositories": repositoriesIds, 
    "users":users, "foundUsers":usersIds,
    "searchedWords":searchedWord})

def checkRepositories(words, request):
    repositories = []
    logged_user = User.objects.get(id = request.user.id)
    all_private_repositories = Repository.objects.all().filter(status = 'private')
    all_public_repositories = Repository.objects.all().filter(status = 'public')
    for r in all_private_repositories:
        developers = User.objects.all().filter(user_developers = r)
        for d in developers:
            if (logged_user.id == d.id):
                for word in words:
                    if (word.lower() in r.name.lower()):
                        if (len(repositories) == 0):
                            repositories.append(r)
                        elif(r not in repositories):
                            repositories.append(r)
    for repository in all_public_repositories:
        for word in words:
            if (word.lower() in repository.name.lower()):
                if (len(repositories) == 0):
                    repositories.append(repository)
                elif(repository not in repositories):
                    repositories.append(repository)
    return repositories

def checkIssues(words):
    issues = []
    all_issues = Issue.objects.all()
    all_public_repositories = Repository.objects.all().filter(status = 'public')
    for r in all_public_repositories:
        for issue in all_issues:
            if (r.id == issue.repository.id):
                for word in words:
                    if (word.lower() in issue.issue_title.lower() or word.lower() in issue.description.lower()):
                        if (len(issues) == 0):
                            issues.append(issue)
                        elif(issue not in issues):
                            issues.append(issue)
    return issues
    
def checkCommits(words):
    commits = [] 
    all_commits = Commit.objects.all()
    all_public_repositories = Repository.objects.all().filter(status = 'public')
    for r in all_public_repositories:
        branch_list = Branch.objects.all().filter(repository = r)
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

def searchedRepositories(request):
    if request.method == 'POST':
       issues, issuesIds,commits,commitsIds,repositories,repositoriesIds,users,usersIds,searchedWords = find_all_searched_results(request)
    return render(request, 'searchedRepositories.html',{"foundCommits":commitsIds, 
    "commits":commits,"foundIssues":issuesIds, "issues":issues,
    "repositories":repositories, "foundRepositories": repositoriesIds, 
    "users": users, "foundUsers":usersIds,
    "searchedWords":searchedWords})

def searchedIssues(request):
    if request.method == 'POST':
       issues, issuesIds,commits,commitsIds,repositories,repositoriesIds,users,usersIds,searchedWords = find_all_searched_results(request)
    return render(request, 'searchedIssues.html',{"foundCommits":commitsIds, 
    "commits":commits,"foundIssues":issuesIds, "issues":issues,
    "repositories":repositories, "foundRepositories": repositoriesIds, 
    "users": users, "foundUsers":usersIds,
    "searchedWords":searchedWords})

def searchedCommits(request):
    if request.method == 'POST':
       issues, issuesIds,commits,commitsIds,repositories,repositoriesIds,users,usersIds,searchedWords = find_all_searched_results(request)
    return render(request, 'searchedCommits.html',{"foundCommits":commitsIds, 
    "commits":commits,"foundIssues":issuesIds, "issues":issues,
    "repositories":repositories, "foundRepositories": repositoriesIds, 
    "users": users, "foundUsers":usersIds,
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

def findRepositories(request):
    foundRepositories = request.POST.get('foundRepositories')
    repositories = []
    if (foundRepositories != '[]'):
        repositoriesFound = foundRepositories.strip('][').split(', ')
        for foundRepository in repositoriesFound:
            repository = get_object_or_404(Repository, id = foundRepository)
            repositories.append(repository)
    return repositories

def findRepositoriesIds(request):
    repositories = findRepositories(request)
    repositoriesIds=[]
    for r in repositories:
        repositoriesIds.append(r.id)
    return repositoriesIds

def go_to_registration(request):
    return render(request, 'registrate.html')

def registrate(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(request, username=username, password=password)

    if user is not None:
        messages.info(request, "User already exist.")
        return render(request, 'registrate.html')
    else :
        user = User.objects.create_user(username,email, password)
        user.last_name = last_name
        user.first_name = first_name
        user.save()
    return redirect('login')

def edit_user(request, id):
    user = User.objects.get(id = id)
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.email = request.POST.get('email')
    user.username = request.POST.get('username')
    password = request.POST.get('password')
    if password != "":
        user.set_password(request.POST.get('password'))
    user.save()
    messages.success(request, 'User has been updated.')
    return redirect("../home/profile")

@login_required(login_url="login")
def go_to_edit_user(request, id):
    if request.user.is_superuser:
        user = User.objects.get(id = id)
        return render(request, 'edit_user.html',{"user_to_edit" : user})
    else:
        return HttpResponse('401 Unauthorized', status=401)

@login_required(login_url="login")
def delete_user(request, id):
    if request.user.is_superuser:
        user = User.objects.get(id = id)
        user.delete()
        messages.success(request, 'User has been deleted.')
        return redirect("/all_users")
    else:
        return HttpResponse('401 Unauthorized', status=401)

@login_required(login_url="login")
def all_users(request):
    if request.user.is_superuser:
        users = User.objects.all()
        return render(request, "all_users.html",{"all_users":users})
    else:
        return HttpResponse('401 Unauthorized', status=401)

def checkUsers(words):
    users = []
    all_users = User.objects.all().filter(is_superuser = False)
    for user in all_users:
        for word in words:
            if (word.lower() in user.username.lower()):
                if (len(users) == 0):
                    users.append(user)
                elif(user not in users):
                    users.append(user)
    return users

def searchedUsers(request):
    if request.method == 'POST':
       issues, issuesIds,commits,commitsIds,repositories,repositoriesIds,users,usersIds,searchedWords = find_all_searched_results(request)
    return render(request, 'searchedUsers.html',{"foundCommits":commitsIds, 
    "commits":commits,"foundIssues":issuesIds, "issues":issues,
    "repositories":repositories, "foundRepositories": repositoriesIds, 
    "users": users, "foundUsers":usersIds,
    "searchedWords":searchedWords})

def findUsers(request):
    foundUsers = request.POST.get('foundUsers')
    users = []
    if (foundUsers != '[]'):
        usersFound = foundUsers.strip('][').split(', ')
        for foundUser in usersFound:
            user = get_object_or_404(User, id = foundUser)
            users.append(user)
    return users

def findUsersIds(request):
    users = findUsers(request)
    usersIds=[]
    for u in users:
        usersIds.append(u.id)
    return usersIds

def visit_profile(request, id):
    user = User.objects.get(id = id)
    user_public_repos = Repository.objects.all().filter(status='public',creator = user)
    logged_user = User.objects.get(id=request.user.id)
    if (user.id == logged_user.id):
        return redirect('/home/profile')
    return render(request,'userProfile.html', {"user":user, "repositories": user_public_repos})

def user_repositories(request,id):
    user = User.objects.get(id = id)
    user_public_repos = Repository.objects.all().filter(status='public', creator = user)
    print(user_public_repos)
    
    return render(request,'userProfile.html', {"user":user, "repositories": user_public_repos})

def find_all_searched_results(request):
    issues = findIssues(request)
    issuesIds = findIssuesIds(request)
    commits = findCommits(request)
    commitsIds = findCommitsIds(request)
    repositories = findRepositories(request)
    repositoriesIds = findRepositoriesIds(request)
    users = findUsers(request)
    usersIds = findUsersIds(request)
    searchedWords = request.POST.get('searchedWords')

    return issues, issuesIds,commits,commitsIds,repositories,repositoriesIds,users,usersIds,searchedWords

def user_projects(request,id):
    user = User.objects.get(id = id)
    user_public_repositories = Repository.objects.all().filter(status='public', creator = user)
    projects = []
    for r in user_public_repositories:
        user_projects = Project.objects.all().filter(repository=r)
        for p in user_projects:
            projects.append(p)
    
    return render(request,'userProjects.html', {"user":user,"projects":projects })
