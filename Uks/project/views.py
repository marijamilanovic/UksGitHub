from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from project.models import Project
from repository.models import Repository

@login_required(login_url="login")
def all_projects(request):
    all_repositories = Repository.objects.all().filter(creator = request.user)
    all_projects = []
    for r in all_repositories:
        all_repo_projects = Project.objects.all().filter(repository = r)
        for p in all_repo_projects:
            all_projects.append(p)
    return render(request,'all_projects.html',{'all_projects':all_projects})

@login_required(login_url="login")
def projects(request,id):
    repository = Repository.objects.get(id=id)
    projects = Project.objects.all().filter(repository = repository)
    return render (request, 'repoProjects.html', {"projects":projects, "repository": repository,"logged_user_id": request.user.id})

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

def closeProject(request,id):
    project = get_object_or_404(Project, id=id)
    project.status = 'Closed'
    project.save()
    return redirect('/project/projects/'+ str(project.repository.id))

def reopenProject(request,id):
    project = get_object_or_404(Project, id=id)
    project.status = 'Opened'
    project.save()
    return redirect('/project/projects/'+ str(project.repository.id))

def getProjectById(request, id):
    project = get_object_or_404(Project, id=id)
    repository = get_object_or_404(Repository, id = project.repository.id)

    return render(request, "updateProject.html", {"project": project, "repository": repository})

def updateProject(request, id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=id)
        project.name = request.POST['name']
        project.description = request.POST['description']
        repository = get_object_or_404(Repository, id = request.POST['repository'] )
        project.save()
        
    return redirect('/project/projects/'+ str(repository.id))
