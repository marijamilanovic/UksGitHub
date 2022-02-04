from django.shortcuts import render, get_object_or_404, redirect
from repository.models import Repository
from .models import Label
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def labels(request,id):
    repository = get_object_or_404(Repository, id=id)
    labels = Label.objects.all().filter(repository = repository)
    return render(request,'labels.html', {"labels": labels, "repository":repository, "logged_user_id": request.user.id})

@login_required(login_url="login")
def newLabel(request,id):
    repository = repository = get_object_or_404(Repository, id=id)
    return render(request,'newLabel.html',{ "repository":repository})

@login_required(login_url="login")
def addLabel(request):
    errorName = None
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        color = request.POST['color']
        repository = get_object_or_404(Repository, id = request.POST['repository'] )
        if name is not None and name == "":
            errorName = "Please enter name!"
            return render(request, "newLabel.html", {"errorName": errorName, "repository":repository})
        newLabel = Label(name = name, description = description, color = color, repository = repository)
        newLabel.save()
        messages.success(request, 'Label has been created.')
    return redirect('/label/labels/'+ str(repository.id))

def getLabelById(request, id):
    label = get_object_or_404(Label, id = id)
    repository = get_object_or_404(Repository, id = label.repository.id)
    labelColor = label.color
    print(labelColor.lower())
    return render(request, "editLabel.html", {"label": label, "repository": repository, "color": labelColor.lower()})

@login_required(login_url="login")
def editLabel(request, id):
    if request.method == 'POST':
        label = get_object_or_404(Label, id = id)
        label.name = request.POST['name']
        label.description = request.POST['description']
        label.color = request.POST['color']
        all_repos = Repository.objects.all()
        for r in all_repos:
            if(r.id == label.repository.id):
                repository = r
        label.save()
        labelsUpdated = labels(request, repository.id)
        messages.success(request, 'Label has been updated.')
    return redirect('/label/labels/'+ str(repository.id))

@login_required(login_url="login")
def deleteLabel(request, id):
    label = get_object_or_404(Label, id = id)
    if not label.repository.developers.all().filter(id=request.user.id):
        return HttpResponse('401 Unauthorized', status=401)
    all_repos = Repository.objects.all()
    for r in all_repos:
        if(r.id == label.repository.id):
            repository = r
    label.delete()
    labelsUpdated = Label.objects.all().filter(repository=label.repository)
    messages.success(request, 'Label has been deleted.')
    return redirect('/label/labels/'+ str(repository.id))