from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from repository.models import Repository
from issue.models import Issue
from commit.models import Commit

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html', {})

def loginUser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.info(request, "Invalid username or password")

    context = {}
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
        repositories = checkRepositories(words)
        issues = checkIssues(words)
        commits = checkCommits(words)
        number_of_repos = len(repositories)
        number_of_issues = len (issues)
        number_of_commits = len(commits)
        issuesIds=[]
        for issu in issues:
            issuesIds.append(issu.id)
        commitsIds=[]
        for c in commits:
            commitsIds.append(c.id)
        repositoriesIds =[]
        for r in repositories:
            repositoriesIds.append(r.id)

    return render(request, 'searchResult.html', {"foundRepos":repositories, "foundRepositoriesNumber":number_of_repos, "foundRepositories":repositoriesIds, 
    "foundIssues": issuesIds,  "foundIssuesNumber" : number_of_issues, "foundCommits": commitsIds, "foundCommitsNumber": number_of_commits,
    "searchedWords":searchedWord})

def checkRepositories(words):
    repositories = []
    all_repositories = Repository.objects.all()
    for repository in all_repositories:
        for word in words:
            if (word.lower() in repository.name.lower()):
                if (len(repositories) == 0):
                    repositories.append(repository)
                else:
                    for r in repositories:
                        if (r.id != repository.id):
                            repositories.append(repository)
    return repositories

def checkIssues(words):
    issues = []
    all_issues = Issue.objects.all()
    for issue in all_issues:
        for word in words:
            if (word.lower() in issue.issue_title.lower()):
                if (len(issues) == 0):
                    issues.append(issue)
                else:
                    for i in issues:
                        if (i.id != issue.id):
                            issues.append(issue)
    return issues
    
def checkCommits(words):
    commits = [] 
    all_commits = Commit.objects.all()
    for commit in all_commits:
        for word in words:
            if (word.lower() in commit.message.lower()):
                if (len(commits) == 0):
                    commits.append(commit)
                else:
                    for c in commits:
                        if (c.id != commit.id):
                            commits.append(commit)
    return commits

def searchedRepositories(request):
    if request.method == 'POST':
       issues = findIssues(request)
       issuesIds = findIssuesIds(request)
       commits = findCommits(request)
       commitsIds = findCommitsIds(request)
       repositories = findRepositories(request)
       repositoriesIds = findRepositoriesIds(request)
       repositoriesNumber = len (repositories)
       commitsNumber = len(commits)
       issuesNumber = len(issues)
       searchedWords = request.POST.get('searchedWords')
    return render(request, 'searchedRepositories.html',{"foundCommits":commitsIds, "foundCommitsNumber":commitsNumber,
    "commits":commits,"foundIssues":issuesIds, "foundIssuesNumber":issuesNumber, "issues":issues,
    "repositories":repositories, "foundRepositories": repositoriesIds, "foundRepositoriesNumber":repositoriesNumber,
    "searchedWords":searchedWords})

def searchedIssues(request):
    if request.method == 'POST':
       issues = findIssues(request)
       issuesIds = findIssuesIds(request)
       commits = findCommits(request)
       commitsIds = findCommitsIds(request)
       repositories = findRepositories(request)
       repositoriesIds = findRepositoriesIds(request)
       repositoriesNumber = len (repositories)
       commitsNumber = len(commits)
       issuesNumber = len(issues)
       searchedWords = request.POST.get('searchedWords')
    return render(request, 'searchedIssues.html',{"foundCommits":commitsIds, "foundCommitsNumber":commitsNumber,
    "commits":commits,"foundIssues":issuesIds, "foundIssuesNumber":issuesNumber, "issues":issues,
    "repositories":repositories, "foundRepositories": repositoriesIds, "foundRepositoriesNumber":repositoriesNumber,
    "searchedWords":searchedWords})

def searchedCommits(request):
    if request.method == 'POST':
       issues = findIssues(request)
       print("NIJE NASAOO")
       issuesIds = findIssuesIds(request)
       commits = findCommits(request)
       commitsIds = findCommitsIds(request)
       repositories = findRepositories(request)
       repositoriesIds = findRepositoriesIds(request)
       repositoriesNumber = len (repositories)
       commitsNumber = len(commits)
       issuesNumber = len(issues)
       searchedWords = request.POST.get('searchedWords')
    return render(request, 'searchedCommits.html',{"foundCommits":commitsIds, "foundCommitsNumber":commitsNumber,
    "commits":commits,"foundIssues":issuesIds, "foundIssuesNumber":issuesNumber, "issues":issues,
    "repositories":repositories, "foundRepositories": repositoriesIds, "foundRepositoriesNumber":repositoriesNumber,
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
    if (foundCommits != '[]'):
        commitsFound = foundCommits.strip('][').split(', ')
        commits = []
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
    if (foundRepositories != '[]'):
        repositoriesFound = foundRepositories.strip('][').split(', ')
        repositories = []
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

