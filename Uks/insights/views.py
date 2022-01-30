from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from repository.models import Repository



def pulse(request, id):
    repository = get_object_or_404(Repository, id=id)



    context = {
        'repository': repository
    }

    return render(request, "insights/base_insights.html", context)












