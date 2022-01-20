from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html', {})

def loginUser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.info(request, "Invalid username or password")

    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    return redirect('/home/')
    #return redirect('index')

def profile(request):
    return redirect('/home/profile')

def go_to_registration(request):
    return render(request, 'registrate.html')

def registrate(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(request, username=username, password=password)

    if user is not None:
        messages.info(request, "User already exist.")
        return render(request, 'registrate.html')
    else :
        user = User.objects.create_user(username,email, password)
        user.last_name = last_name
        user.first_name = first_name
        user.save()
    return redirect('login')
