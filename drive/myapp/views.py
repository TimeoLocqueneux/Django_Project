import os
from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def main(request):
    # Obtenir le chemin absolu du répertoire source du projet
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Naviguer dans le sous-dossier 'myapp'
    images_pour_site = os.path.join(project_root, 'myapp', 'static', 'img')
    
    # Lister les fichiers et les dossiers dans le sous-dossier 'myapp'
    files = os.listdir(images_pour_site)
    
    return render(request, 'main.html', {'files': files, 'directory': images_pour_site})

def profile(request):
    return render(request, "profile.html")
