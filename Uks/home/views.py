from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader

from django.contrib.auth.decorators import login_required

from Uks.decorators import authorized

# Create your views here.


@login_required(login_url="login")
def index(request):
    template = loader.get_template('home/index.html')
    return render(request, "home/index.html", {})