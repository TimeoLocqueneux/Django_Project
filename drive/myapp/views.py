import shutil 
import os
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import JsonResponse
from datetime import datetime
from.models import Fichier, Dossier

# Create your views here.
from django.contrib.auth import authenticate, login
from .forms import RegisterForm,LoginForm
from .models import User  # Assuming you have a User model
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User




def login_register_view(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = RegisterForm(request.POST)
            login_form = LoginForm()
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, "Inscription réussie ! Vous êtes maintenant connecté.")
                return redirect('main')
            else:
                messages.error(request, "Il y a eu une erreur avec votre inscription.")
                
        elif 'login' in request.POST:
            login_form = LoginForm(request.POST)
            register_form = RegisterForm()
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                
                # Authentification
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Connexion réussie !")
                    return redirect('main')
                else:
                    messages.error(request, "Email ou mot de passe invalide.")
                    print("Authentification échouée pour l'email :", email)  # Debug
                    return redirect('main')
            else:
                print("Le formulaire de connexion n'est pas valide.", login_form.errors)  # Debug

    else:
        register_form = RegisterForm()
        login_form = LoginForm()
    
    return render(request, 'login.html', {
        'register_form': register_form,
        'login_form': login_form
    })








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

