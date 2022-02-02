from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template import loader

from .models import Repository

from .forms import BranchForm
from .forms import EditBranchForm


from .models import Branch

from django.core.exceptions import ValidationError



def createBranch(request, id):
    form = BranchForm()
    print('FORM DATA:', id) 
    repository = get_object_or_404(Repository, id=id)
    error_name = False
    error_name_message = "Branch with same name already exist in repository"

    if request.method == 'POST':                            #Provera da li je POST
        print('FORM DATA:', request.POST)                   #Print forme - radi provere
        form = BranchForm(request.POST)  
        branch_list = Branch.objects.all().filter(repository = repository)
        same_name = any(b.name == request.POST["name"] for b in branch_list)

        if same_name:
            error_name = True
        else:
            error_name = False

        if form.is_valid() and not same_name:                                 #Validacija polja forme
            branch = Branch.objects.create(
                name = request.POST['name'],
                repository = Repository.objects.get(pk = id)
            )                                                                   #Cuvanje u bazi
            return redirect('branch:repoBranchList', id = id)
        
    context = {
        'form': form,
        'repository': repository,
        'error_name': error_name,
        'error_name_message': error_name_message,
        }
    return render(request, "branch/createBranch.html", context)


def branchList(request):
    branch_list = Branch.objects.all() 
    context = {
        'branch_list': branch_list,
    }
    return render(request, "branch/branchList.html", context)


def deleteBranch(request, id):
    Branch.objects.get(pk=id).delete()
    return render(request, "branch/repoBranchList.html", context)


def repoBranchList(request, id):
    repo = get_object_or_404(Repository, id=id)
    branch_list = Branch.objects.all().filter(repository=repo)
    context = {
        'branch_list': branch_list,
        'repository': repo,
    }
    return render(request, "branch/repoBranchList.html", context)


def editBranch(request, id):
    branch = get_object_or_404(Branch, id=id)
    repo = get_object_or_404(Repository, id = branch.repository.id)
    branch_list = Branch.objects.all().filter(repository=repo)
    error_name = False
    error_name_message = "Branch with same name already exist in repository"

    if request.method == 'POST':                            
        form = EditBranchForm(request.POST)  
        same_name = any(b.name == request.POST["name"] for b in branch_list)

        if request.POST["name"] == branch.name:
            same_name = False

        if same_name:
            error_name = True
        else:
            error_name = False

        if form.is_valid() and not same_name:
            print(request.POST)
            name = request.POST["name"]
            #is_default = request.POST["is_default"] 
            branch = Branch.objects.get(pk = id)
            branch.name = name
            if 'is_default' in request.POST:
                branch.is_default = True;
                branch_repo_list = Branch.objects.all().filter(is_default = True)
                for branchR in branch_repo_list:
                    branchR.is_default = False
                    branchR.save()
            
            branch.save()
                                                                              
            return redirect('branch:repoBranchList', id = branch.repository.id)


    my_record = Branch.objects.get(pk=id)
    form = EditBranchForm(instance=my_record)

    if branch.is_default:
        form = BranchForm(instance=my_record)

    context = {
        'form': form,
        'repository': repo,
        'error_name': error_name,
        'error_name_message': error_name_message,
        }  


    return render(request, "branch/editBranch.html", context)



    










