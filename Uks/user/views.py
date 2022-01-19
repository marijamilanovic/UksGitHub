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
    #return redirect('index')

def profile(request):
    return redirect('/home/profile')

def search(request):
    if request.method == 'POST':
        searchedWord = request.POST['search']
        words = searchedWord.split()
        repositories = []
        issues = []
        commits = []
        all_repositories = Repository.objects.all()
        for repository in all_repositories:
            for word in words:
                if (word.lower() in repository.name.lower()):
                    #ako se rec sadrzi negde u nazivu stringa
                    #ubaci taj repo u listu rezultata koju vracas
                    #proveri da li je u listu vec dodat taj repo za neku rec
                    if (len(repositories) == 0):
                        repositories.append(repository)
                    else:
                        for r in repositories:
                            if (r.id != repository.id):
                                repositories.append(repository)
        all_issues = Issue.objects.all()
        for issue in all_issues:
            for word in words:
                if (word.lower() in issue.issue_title.lower()):
                    #ako se rec sadrzi negde u nazivu stringa
                    #ubaci taj repo u listu rezultata koju vracas
                    #proveri da li je u listu vec dodat taj repo za neku rec
                    if (len(issues) == 0):
                        issues.append(issue)
                    else:
                        for i in issues:
                            if (i.id != issue.id):
                                issues.append(issue)
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
        number_of_repos = len(repositories)
        number_of_issues = len (issues)
        number_of_commits = len(commits)
        issuesIds=[]
        for issu in issues:
            issuesIds.append(issu.id)
        commitsIds=[]
        for c in commits:
            commitsIds.append(c.id)
    return render(request, 'searchResult.html', {"foundRepos":repositories, "foundRepositoriesNumber":number_of_repos, 
    "foundIssues": issuesIds,  "foundIssuesNumber" : number_of_issues, "foundCommits": commitsIds, "foundCommitsNumber": number_of_commits})

def searchedIssues(request):
    if request.method == 'POST':
        foundIssues = request.POST.get('foundIssues')
        foundCommits = request.POST.get('foundCommits')
        issuesFound = foundIssues.strip('][').split(', ')
        issues = []
        commitsFound = foundCommits.strip('][').split(', ')
        commits = []
        for foundIssue in issuesFound:
            issue = get_object_or_404(Issue, id = foundIssue)
            issues.append(issue)
            issuesNumber = len(issues)
        for foundCommit in commitsFound:
            commit = get_object_or_404(Commit, id = foundCommit)
            commits.append(commit)
            commitsNumber = len(commits)
        issuesIds=[]
        commitsIds=[]
        for issu in issues:
            issuesIds.append(issu.id)
        commitsIds=[]
        for c in commits:
            commitsIds.append(c.id)
        
    return render(request, 'searchedIssues.html',{"foundIssues":issuesIds, "foundIssuesNumber":issuesNumber, "issues":issues,
    "foundCommits":commitsIds, "foundCommitsNumber":commitsNumber, "commits":commits })

def searchedCommits(request):
    if request.method == 'POST':
        foundCommits = request.POST.get('foundCommits')
        foundIssues = request.POST.get('foundIssues')
        commitsFound = foundCommits.strip('][').split(', ')
        commits = []
        issuesFound = foundIssues.strip('][').split(', ')
        issues = []
        for foundIssue in issuesFound:
            issue = get_object_or_404(Issue, id = foundIssue)
            issues.append(issue)
            issuesNumber = len(issues)
        for foundCommit in commitsFound:
            commit = get_object_or_404(Commit, id = foundCommit)
            commits.append(commit)
            commitsNumber = len(commits)
        issuesIds=[]
        commitsIds=[]
        for issu in issues:
            issuesIds.append(issu.id)
        commitsIds=[]
        for c in commits:
            commitsIds.append(c.id)
        
    return render(request, 'searchedCommits.html',{"foundCommits":commitsIds, "foundCommitsNumber":commitsNumber,"commits":commits,
    "foundIssues":issuesIds, "foundIssuesNumber":issuesNumber, "issues":issues})