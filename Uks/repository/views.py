from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from .models import Repository

# Create your views here.

@login_required(login_url="login")
def index(request):
    template = loader.get_template('repository/index.html')
    return render(request, "repository/index.html", {})
