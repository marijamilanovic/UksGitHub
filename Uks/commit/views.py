from email import message
from multiprocessing import context
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from branch.models import Branch
from django.contrib.auth.models import User
from .forms import CommitForm
from .models import Commit
from datetime import date, datetime
import hashlib
from repository.models import Repository


@login_required(login_url="login")
def createCommit(request, id):
    form = CommitForm()
    branch = get_object_or_404(Branch, id=id)
    repository = get_object_or_404(Repository, id=branch.repository.id)

    if request.method == 'POST':
        if request.user in list(repository.developers.all()):                            
            #print('FORM DATA:', request.POST)                   
            form = CommitForm(request.POST) 
            print("Commit object: " + form.data.__str__())                    
            if form.is_valid():
                now = datetime.now()

                commit = Commit.objects.create(
                    message = request.POST['message'],
                    branch = Branch.objects.get(pk = id),
                    date_time = datetime.now(),
                    hash_id = " ", 
                    author = User.objects.get(pk = request.user.id),
                    repository = Repository.objects.get(pk = branch.repository.id)
                )

                print("commit id: ",  str(commit.pk))

                hash = hashlib.sha1(str(commit.pk).encode('utf-8'))

                commit.hash_id = hash.hexdigest()

                commit.save()

                return redirect('commit:commitList', id=branch.id)
        else:
            return HttpResponse("Authorization failed!")
        
    context = {
        'form': form,
        'repository': repository,
        'branch': branch,
    }
    return render(request, "commit/createCommit.html", context)


def commitList(request, id):
    branch = get_object_or_404(Branch, id=id)
    commit_list = Commit.objects.all().filter(branch = branch) 
    context = {
        'commit_list': commit_list,
        'repository': branch.repository,
        'branch': branch,
    }
    return render(request, "commit/commitList.html", context)

@login_required(login_url="login")
def deleteCommit(request, id):
    commit = get_object_or_404(Commit, id=id)
    branch = get_object_or_404(Branch, id=commit.branch.id)
    repository = get_object_or_404(Repository, id=branch.repository.id)
    if request.user in list(repository.developers.all()): 
        Commit.objects.get(pk=id).delete()
        return redirect('commit:commitList', id=commit.branch.id)
    else:
        return HttpResponse("Authorization failed!")


@login_required(login_url="login")
def get_current_repository(repo_id):
    return get_object_or_404(Repository, id = repo_id)


def viewFoundCommit(request, id):
    commit = get_object_or_404(Commit, id = id)
    branch = get_object_or_404(Branch, commit = commit)
    return render(request, 'commit/viewFoundCommit.html', {'commit':commit, 'repository': get_current_repository(branch.repository.id), 'branch':branch})
