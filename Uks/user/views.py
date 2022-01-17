from django.shortcuts import render, redirect

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
        print(words)
        print(words[0])
        i = len(words)
        repositories = []
        issues = []
        commits = []
        all_repositories = Repository.objects.all()
        for repository in all_repositories:
            if (words[i-1].lower() in repository.name.lower()):
                #ako se rec sadrzi negde u nazivu stringa
                #ubaci taj repo u listu rezultata koju vracas
                repositories.append(repository)
                print('NASAOOO')
        all_issues = Issue.objects.all()
        for issue in all_issues:
            if ((words[i-1].lower() in issue.issue_title) or (words[i-1].lower() in issue.description)):
                issues.append(issue)
                print('NASAOOO ISSUE')
        all_commits = Commit.objects.all()
        for commit in all_commits:
            if (words[i-1].lower() in commit.message):
                commits.append(commit)
                print('NASAOOO COMMIT')

    return render(request, 'searchResult.html', {})
