import django.contrib.auth.backends
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from users.services.filters import UserFilter
from django.shortcuts import get_object_or_404
from users.services.distance import get_coords
from users.services.emailsender import send_emails_to_users
from .forms import SignUpForm
from .models import CustomUser, Matches


# Create your views here
def index(request):
    return render(request, "users/index.html")

# api/clients/create
def create(request):
    """Creating new user of application"""
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.lat, user.lng = get_coords(request)
            user.save()
            login(request, user, backend=django.contrib.auth.backends.ModelBackend)
    else:
        form = SignUpForm()
    return render(request, 'users/create.html', {'form': form})

# api/clients/login
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
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# api/clients/logout
def log_out(request):
    logout(request)
    return redirect('index')

# api/clients/<int:user_id>
def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, "users/profile.html", {'user': user})

# api/clients/<int:user_id>/match
def match(request, user_id):
    """If two users like each other, message will be sent to both of them"""
    current_user = CustomUser.objects.get(id=request.user.id)
    liked_user = CustomUser.objects.get(id=user_id)

    if not Matches.objects.filter(first_user=current_user, second_user=liked_user):
        Matches.objects.create(first_user=current_user, second_user=liked_user)

    if Matches.objects.filter(first_user=liked_user, second_user=current_user):
        send_emails_to_users(current_user, liked_user)
        send_emails_to_users(liked_user, current_user)

    return redirect('index')

# api/clients/list
def users_list(request):
    """Renders page with all users in database, with the possibility of filtration"""
    users_filter = UserFilter(request.GET, queryset=CustomUser.objects.filter(is_admin=False), request=request)
    return render(request, 'users/list.html', {'filter': users_filter})
