from multiprocessing import context
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template import loader

from .forms import BranchForm

from .models import Branch



def createBranch(request):
    form = BranchForm()

    if request.method == 'POST':                            #Provera da li je POST
        print('FORM DATA:', request.POST)                   #Print forme - radi provere
        form = BranchForm(request.POST)                     
        if form.is_valid():                                 #Validacija polja forme
            form.save()                                     #Cuvanje u bazi
            return redirect('profile')
        
    context = {'form': form}
    return render(request, "branch/createBranch.html", context)













