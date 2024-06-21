from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import set_database_connection
from .models import UserProfile
# Create your views here.


def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_profile = user.userprofile
            login(request, user)
            try:
                role = user_profile.user_type
                set_database_connection(role)
                messages.success(request, f'Вітаємо, {user_profile.user}!')
            except UserProfile.DoesNotExist:
                messages.error(request, 'Такого користувача не існує')
            return redirect('analytics')
        else:
            messages.error(request, 'Неправильний логін або пароль!')
            return redirect('home')
    else:
        return render(request, 'home.html')


def logout_user(request):
    set_database_connection('connection')
    logout(request)
    messages.success(request, 'Ви вийшли з системи!')
    return redirect('home')
