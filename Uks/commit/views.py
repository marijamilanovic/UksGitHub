from email import message
from multiprocessing import context
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template import loader

from branch.models import Branch
from django.contrib.auth.models import User


from .forms import CommitForm

from .models import Commit

from datetime import date, datetime

import hashlib



def createCommit(request):
    form = CommitForm()

    if request.method == 'POST':                            
        #print('FORM DATA:', request.POST)                   
        form = CommitForm(request.POST) 
        print("Commit object: " + form.data.__str__())                    
        if form.is_valid():
            now = datetime.now()

            commit = Commit.objects.create(
                message = request.POST['message'],
                branch = Branch.objects.get(pk = request.POST['branch']),
                date_time = datetime.now(),
                hash_id = " ", 
                author = User.objects.get(pk = request.user.id)
            )

            print("commit id: ",  str(commit.pk))

            hash = hashlib.sha1(str(commit.pk).encode('utf-8'))

            commit.hash_id = hash.hexdigest()

            commit.save()

            return redirect('commit:commitList')
        
    context = {'form': form}
    return render(request, "commit/createCommit.html", context)


def commitList(request):
    commit_list = Commit.objects.all() 
    context = {
        'commit_list': commit_list,
    }
    return render(request, "commit/commitList.html", context)


def deleteCommit(request, id):
    Commit.objects.get(pk=id).delete()
    return redirect('commit:commitList')
