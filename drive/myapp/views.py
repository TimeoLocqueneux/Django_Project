import os
import tkinter as tk
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import JsonResponse
from datetime import datetime
from.models import Fichier, Dossier

# Create your views here.
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from datetime import datetime
from .forms import RegisterForm,LoginForm
from .models import User  # Assuming you have a User model
from tkinter import filedialog

def get_files_info(directory):
    files_info = []
    for root, dirs, files in os.walk(directory):
        if root != directory:
            dirs.clear()  # Prevents os.walk from going into subdirectories
            continue
        for name in files:
            file_path = os.path.join(root, name)
            file_size = os.path.getsize(file_path)
            file_mtime = os.path.getmtime(file_path)
            file_mtime = datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d')
            files_info.append({
                'name': os.path.relpath(file_path, directory),
                'size': (file_size / 1000).__int__(),
                'mtime': file_mtime,
                'type': 'file'
            })
        for name in dirs:
            dir_path = os.path.join(root, name)
            dir_size = sum(os.path.getsize(os.path.join(dir_path, f)) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)))
            dir_mtime = os.path.getmtime(dir_path)
            dir_mtime = datetime.fromtimestamp(dir_mtime).strftime('%Y-%m-%d')
            files_info.append({
                'name': os.path.relpath(dir_path, directory),
                'size': (dir_size / 1000).__int__(),
                'mtime': dir_mtime,
                'type': 'directory'
            })
    return files_infofrom django.contrib import messages
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
    
    base_dir = os.path.join(project_root, 'uploads')
    current_dir = os.path.join(base_dir, path)
    
    if not os.path.exists(current_dir):
        current_dir = base_dir
    
   
    drive_index = current_dir.find('uploads')
    if drive_index != -1:
        cut_directory = current_dir[drive_index + len('uploads') + 1:]
        cut_directory2 = cut_directory
    if not cut_directory:
        cut_directory = None
        cut_directory2 = ''
 

    files_info = get_files_info(current_dir)

    return render(request, 'main.html', {'files': files_info, 'directory': current_dir, 'cut_directory' : cut_directory, 'cut_directory2': cut_directory2} )

def profile(request):
    return render(request, "profile.html")

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


def import_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        path = request.POST.get('path', '')
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = os.path.join(project_root, 'uploads')
        current_dir = os.path.join(base_dir, path)
        
        if not os.path.exists(current_dir):
            current_dir = base_dir
        
        file_path = os.path.join(current_dir, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        return redirect('main_with_path', path=path)
    return render(request, 'main.html', {'error': 'Aucun fichier sélectionné.'})

def create_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        path = request.POST.get('path', '')

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = os.path.join(project_root, 'uploads')
        current_dir = os.path.join(base_dir, path)
        
        folder_path = os.path.join(current_dir, folder_name)
        
        if folder_name and not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return redirect('main_with_path', path=path)
        else:
            error_message = "Nom de dossier invalide ou dossier existe déjà."
            return render(request, 'main.html', {'error': error_message, 'path': path})

    return redirect('main')
