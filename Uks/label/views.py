from django.shortcuts import render, get_object_or_404, redirect
from repository.models import Repository
from .models import Label

def labels(request,id):
    repository = get_object_or_404(Repository, id=id)
    labels = Label.objects.all().filter(repository = repository)
    return render(request,'labels.html', {"labels": labels, "repository":repository})

def newLabel(request,id):
    repository = repository = get_object_or_404(Repository, id=id)
    return render(request,'newLabel.html',{ "repository":repository})

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
    return redirect('/label/labels/'+ str(repository.id))