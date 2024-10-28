import os
from django.shortcuts import render, HttpResponse
from datetime import datetime

# Create your views here.
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
