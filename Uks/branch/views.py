from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template import loader

from .models import Repository

from .forms import BranchForm

from .models import Branch



def createBranch(request, id):
    form = BranchForm()

    if request.method == 'POST':                            #Provera da li je POST
        #print('FORM DATA:', request.POST)                   #Print forme - radi provere
        form = BranchForm(request.POST)                     
        if form.is_valid():                                 #Validacija polja forme
            branch = Branch.objects.create(
                name = request.POST['name'],
                repository = Repository.objects.get(pk = id)
            )                                                #Cuvanje u bazi
            return redirect('branch:repoBranchList', id = id)
        
    context = {'form': form}
    return render(request, "branch/createBranch.html", context)


def branchList(request):
    branch_list = Branch.objects.all() 
    context = {
        'branch_list': branch_list,
    }
    return render(request, "branch/branchList.html", context)


def deleteBranch(request, id):
    Branch.objects.get(pk=id).delete()
    return redirect('branch:branchList')


def repoBranchList(request, id):
    repo = get_object_or_404(Repository, id=id)
    branch_list = Branch.objects.all().filter(repository=repo)
    context = {
        'branch_list': branch_list,
        'repository': repo,
    }
    return render(request, "branch/repoBranchList.html", context)

    










