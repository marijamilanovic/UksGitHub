from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from project.models import Project
from repository.models import Repository


def all_projects(request):
    all_projects = Project.objects.all()
    return render(request,'all_projects.html',{'all_projects':all_projects})

def projects(request,id):
    repository = Repository.objects.get(id=id)
    projects = Project.objects.all().filter(repository = repository)
    return render (request, 'repoProjects.html', {"projects":projects, "repository": repository})

def newProject(request, id):
    repository = get_object_or_404(Repository, id=id)
    return render(request, 'newProject.html', { "repository":repository, "logged_user_id": request.user.id})

def addProject(request):
    errorName = None
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        repository = get_object_or_404(Repository, id = request.POST['repository'] )
        if name is not None and name == "":
            errorName = "Please enter name!"
            return render(request, "newProject.html", {"errorName": errorName, "repository":repository})
        else:
            if description=="":
                newProject = Project(name = name, repository = repository)
            else:
                newProject = Project(name = name, description = description, repository = repository)
            newProject.save()
    
    return redirect('/project/projects/'+ str(repository.id))
