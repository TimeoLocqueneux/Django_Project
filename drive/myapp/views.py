import os
from django.shortcuts import render, HttpResponse
from datetime import datetime

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm,LoginForm
from .models import User  # Assuming you have a User model



def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def main(request):
    # Obtenir le chemin absolu du répertoire source du projet
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Naviguer dans le sous-dossier 'myapp/static/img'
    images_pour_site = os.path.join(project_root, 'myapp', 'static', 'img')
    
    # Lister les fichiers et les dossiers dans le sous-dossier 'myapp/static/img'
    files_info = []
    for file_name in os.listdir(images_pour_site):
        file_path = os.path.join(images_pour_site, file_name)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            file_mtime = os.path.getmtime(file_path)
            file_mtime = datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d')
            files_info.append({
                'name': file_name,
                'size': (file_size/1000).__int__(),
                'mtime': file_mtime
            })
    
    return render(request, 'main.html', {'files': files_info, 'directory': images_pour_site})

def profile(request):
    return render(request, "profile.html")

    register_form = UserForm()
    login_form = LoginForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = UserForm(request.POST)
            if register_form.is_valid():
                email = register_form.cleaned_data['email']
                password = register_form.cleaned_data['password']
                User.objects.create(email=email, password=password)
                return redirect('home')
        elif 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                try:
                    user = User.objects.get(email=email)
                    if user.password == password:
                        return redirect('success')
                    else:
                        login_form.add_error('password', 'Incorrect password')
                except User.DoesNotExist:
                    login_form.add_error('email', 'Email not found')

    return render(request, 'home.html', {'register_form': register_form, 'login_form': login_form})

def success_view(request):
    return render(request, 'success.html')

def register_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create(email=email, password=password)
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.password == password:
                    return redirect('success')
                else:
                    form.add_error('password', 'Incorrect password')
            except User.DoesNotExist:
                form.add_error('email', 'Email not found')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})