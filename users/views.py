from os import add_dll_directory
from django.contrib import auth
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import SignUpForm
from .models import CustomUser, Matches
from .emailsender import EmailSender

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

def create(request):
    """Создание нового пользователя приложения"""
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

def user_profile(request, user_id):
    """Профиль отдельного пользователя"""
    try:
        user = CustomUser.objects.get(id=user_id)
    except Exception as e:
        raise e
    return render(request, "users/profile.html", {'user': user})

def match(request, user_id):
    """Вызывается если один участник поставил лайк другому"""
    current_user = CustomUser.objects.get(id=request.user.id)
    liked_user = CustomUser.objects.get(id=user_id)

    #Проверяем есть ли в базе уже информация
    if not Matches.objects.filter(first_user=current_user, second_user=liked_user):
        Matches.objects.create(first_user=current_user, second_user=liked_user)

    #Проверяем есть ли взаимная симпатия у участников
    if Matches.objects.filter(first_user=liked_user, second_user=current_user):
        EmailSender.send_emails_to_users(current_user, liked_user)
        EmailSender.send_emails_to_users(liked_user, current_user)

    return redirect('index')