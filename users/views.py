from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import set_database_connection
from .models import CustomUser
from template_views import *


def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            role = user.role
            request.session['username'] = username
            login(request, user)
            try:
                set_database_connection(role)
                if role == "master":
                    master_user_id = user.master_id.id_master
                    request.session['master_user_id'] = master_user_id
                messages.success(request, f'Вітаємо, {username}!')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Такого користувача не існує')
            return redirect('registrations')
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
