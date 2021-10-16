from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from .models import CustomUser


# Create your views here.
def index(request):
    return render(request, 'users/index.html')

def create(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            new_user = authenticate(email=email, password=password)
            login(request, new_user)
    else:
        form = SignUpForm()
    return render(request, 'users/create.html', {'form':form})

def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return redirect('create')
        else:
            print('form is not valid')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form':form})

def log_out(request):
    logout(request)
    return redirect('index')