from django.shortcuts import render, get_object_or_404, redirect
from repository.models import Repository
from .models import Label

def labels(request,id):
    repository = get_object_or_404(Repository, id=id)
    labels = Label.objects.all().filter(repository = repository)
    return render(request,'labels.html', {"labels": labels, "repository":repository})