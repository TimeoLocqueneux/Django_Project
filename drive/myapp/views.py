import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import json
import logging
import shutil

base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')

def authenticate_with_email(request, email=None, password=None):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None

    if user.check_password(password):
        return user
    return None


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
            file_mtime = datetime.fromtimestamp(file_mtime).strftime('%d-%m-%Y')
            file_type = (
                'video' if name.endswith(('.avi', '.mp4', '.mkv', '.mov', '.wmv', '.flv', '.mpeg', '.webm')) else
                'image' if name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')) else
                'texte' if name.endswith('.txt') else
                'pdf' if name.endswith('.pdf') else
                'excel' if name.endswith(('.csv', '.xlsx', '.xls', '.ods')) else
                'audio' if name.endswith(('.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma')) else
                'doc' if name.endswith(('.doc', '.docx', '.odt')) else
                'ppt' if name.endswith(('.ppt', '.pptx', '.odp')) else
                'other'
                )
            files_info.append({
                'name': os.path.relpath(file_path, directory),
                'size': (file_size / 1000).__int__(),
                'mtime': file_mtime,
                'type': 'file',
                'file_type': file_type
            })
        for name in dirs:
            dir_path = os.path.join(root, name)
            dir_size = sum(os.path.getsize(os.path.join(dir_path, f)) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)))
            dir_mtime = os.path.getmtime(dir_path)
            dir_mtime = datetime.fromtimestamp(dir_mtime).strftime('%d-%m-%Y')
            files_info.append({
                'name': os.path.relpath(dir_path, directory),
                'size': (dir_size / 1000).__int__(),
                'mtime': dir_mtime,
                'type': 'directory',
                'file_type': 'directory'
            })
    return files_info


logger = logging.getLogger(__name__)

def login_register_view(request):
    global base_dir
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = RegisterForm(request.POST)
            login_form = LoginForm()
            if register_form.is_valid():
                user = register_form.save()
                user_dir = os.path.join(base_dir, user.username)
                os.makedirs(user_dir)
                base_dir = user_dir
                login(request, user)
                messages.success(request, "Inscription réussie ! Vous êtes maintenant connecté.")
                return redirect('main')
            else:
                messages.error(request, "Il y a eu une erreur avec votre inscription.")
        elif 'login' in request.POST:
            login_form = LoginForm(request.POST)
            register_form = RegisterForm()
            if login_form.is_valid():
                email = login_form.cleaned_data.get('email')
                password = login_form.cleaned_data.get('password')
                logger.debug(f"Trying to authenticate email: {email}")
                user = authenticate_with_email(request, email=email, password=password)
                if user is not None:
                    base_dir= os.path.join(base_dir, user.username)
                    login(request, user)
                    messages.success(request, "Connexion réussie !")
                    return redirect('main')
                else:
                    logger.debug(f"Authentication failed for email: {email}")
                    messages.error(request, "Email ou mot de passe incorrect.")
            else:
                logger.debug(f"Login form is invalid: {login_form.errors}")
                messages.error(request, "Il y a eu une erreur avec votre connexion.")
    else:
        register_form = RegisterForm()
        login_form = LoginForm()

    return render(request, 'login.html', {'register_form': register_form, 'login_form': login_form})

@login_required(login_url='login')
def main(request, path=''):


    current_dir = os.path.join(base_dir, path)

    if not os.path.exists(current_dir):
        current_dir = base_dir

    drive_index = current_dir.find('uploads')
    if drive_index != -1:
        cut_directory = current_dir[drive_index + len('uploads') + len(request.user.username)+ 2:]
        cut_directory2 = current_dir[drive_index + len('uploads') + 1:]
    if not cut_directory:
        cut_directory = None
        cut_directory2 = request.user.username 
        
    uploads_index = current_dir.find('uploads')
    if uploads_index != -1:
        viewer_path = current_dir[uploads_index:].replace('\\', '/')
    else:
        viewer_path = current_dir.replace('\\', '/')

    files_info = get_files_info(current_dir)

    search_query = request.GET.get('search', '').lower()
    if search_query:
        files_info = [f for f in files_info if search_query in f['name'].lower()]

    directories = [f for f in files_info if f['type'] == 'directory']
    files = [f for f in files_info if f['type'] == 'file']

    directories.sort(key=lambda x: x['name'].lower())
    sort_by = request.GET.get('sort', 'name')
    reverse = request.GET.get('order', 'asc') == 'desc'
    if sort_by == 'size':
        files.sort(key=lambda x: x['size'], reverse=reverse)
    elif sort_by == 'date':
        files.sort(key=lambda x: datetime.strptime(x['mtime'], '%d-%m-%Y'), reverse=reverse)
    elif sort_by == 'type':
        files.sort(key=lambda x: x['file_type'], reverse=reverse)
    else:
        files.sort(key=lambda x: x['name'].lower(), reverse=reverse)

    files_info = directories + files
            
    return render(request, 'main.html', {'files': files_info, 'directory': current_dir, 'cut_directory' : cut_directory, 'cut_directory2': cut_directory2, 'viewer_path': viewer_path, 'sort_by': sort_by, 'order': 'desc' if reverse else 'asc', 'search_query': search_query} )

def count_files_by_type(directory):
    file_counts = {
        'video': 0,
        'image': 0,
        'texte': 0,
        'pdf': 0,
        'excel': 0,
        'audio': 0,
        'doc': 0,
        'ppt': 0,
        'other': 0
    }
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_type = (
                'video' if name.endswith(('.avi', '.mp4', '.mkv', '.mov', '.wmv', '.flv', '.mpeg', '.webm')) else
                'image' if name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')) else
                'texte' if name.endswith('.txt') else
                'pdf' if name.endswith('.pdf') else
                'excel' if name.endswith(('.csv', '.xlsx', '.xls', '.ods')) else
                'audio' if name.endswith(('.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma')) else
                'doc' if name.endswith(('.doc', '.docx', '.odt')) else
                'ppt' if name.endswith(('.ppt', '.pptx', '.odp')) else
                'other'
                )
            file_counts[file_type] += 1
    return file_counts

def count_sizes_by_type(directory):
    file_sizes = {
        'video': 0,
        'image': 0,
        'texte': 0,
        'pdf': 0,
        'excel': 0,
        'audio': 0,
        'doc': 0,
        'ppt': 0,
        'other': 0
    }
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_type = (
                'video' if name.endswith(('.avi', '.mp4', '.mkv', '.mov', '.wmv', '.flv', '.mpeg', '.webm')) else
                'image' if name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')) else
                'texte' if name.endswith('.txt') else
                'pdf' if name.endswith('.pdf') else
                'excel' if name.endswith(('.csv', '.xlsx', '.xls', '.ods')) else
                'audio' if name.endswith(('.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma')) else
                'doc' if name.endswith(('.doc', '.docx', '.odt')) else
                'ppt' if name.endswith(('.ppt', '.pptx', '.odp')) else
                'other'
                )
            file_sizes[file_type] += (os.path.getsize(os.path.join(root, name))/ 1000000).__round__(2)
    return file_sizes

def calculate_total_storage_used(user,directory):
    total_storage = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            total_storage += os.path.getsize(os.path.join(root, file))
    return (total_storage / 1000000).__round__(2)

def calculate_cumulative_storage_over_time(directory):
    all_dates = []

    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            file_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d-%m-%Y')
            if file_date not in all_dates:
                all_dates.append(file_date)
    sorted_dates = sorted(all_dates, key=lambda date: datetime.strptime(date, '%d-%m-%Y'))

    start_date = datetime.strptime(sorted_dates[0], '%d-%m-%Y')
    end_date = datetime.now()
    current_date = start_date
    while current_date <= end_date:
        if current_date.strftime('%d-%m-%Y') not in all_dates:
            all_dates.append(current_date.strftime('%d-%m-%Y'))
        current_date += timedelta(days=1)
    all_dates.sort(key=lambda date: datetime.strptime(date, '%d-%m-%Y'))
    
    cumulative_storage_over_time = []
    cumulative_sum = 0
    for date in all_dates:
        daily_storage = calculate_storage_by_date(directory, date)
        cumulative_sum += daily_storage
        cumulative_storage_over_time.append({'date': date, 'cumulative_storage': cumulative_sum})

    return cumulative_storage_over_time

def calculate_storage_by_date(directory, target_date):
    total_size = 0
    target_date = datetime.strptime(target_date, '%d-%m-%Y')
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            file_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d-%m-%Y')
            if datetime.strptime(file_date, '%d-%m-%Y') == target_date:
                total_size += os.path.getsize(file_path)
    return (total_size / 1000000).__round__(2)

def profile(request):
    total_storage_used = calculate_total_storage_used(request.user,base_dir)
    max_storage = 100
    file_counts = count_files_by_type(base_dir)
    file_sizes = count_sizes_by_type(base_dir)
    storage_percentage = (total_storage_used / max_storage) * 100
    empty_percentage = ((max_storage - total_storage_used) / max_storage) * 100
    storage_over_time = calculate_cumulative_storage_over_time(base_dir)
    return render(request, "profile.html", {'file_counts': file_counts, 'file_sizes':file_sizes, 'total_storage_used': total_storage_used, 'max_storage': max_storage, 'remaining_storage': max_storage - total_storage_used, 'storage_percentage': storage_percentage, 'empty_percentage': empty_percentage, 'storage_over_time': storage_over_time})



def rename_file(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        new_name = body.get('new_name')
        path = body.get('path', '')
        old_name = body.get('old_name', '')
        current_dir = os.path.join(base_dir, path)
        old_file_path = os.path.join(current_dir, old_name)
        new_file_path = os.path.join(current_dir, new_name)
        if new_name and not os.path.exists(new_file_path):
            os.rename(old_file_path, new_file_path)
            return redirect('main_with_path', path=path)
        else:
            error_message = "Nom de fichier invalide ou fichier existe déjà."
            return render(request, 'main.html', {'error': error_message, 'path': path})
    return redirect('main')

def delete_file(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        file_name = body.get('file_name')
        path = body.get('path', '')
        current_dir = os.path.join(base_dir, path)
        file_path = os.path.join(current_dir, file_name)
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                os.rmdir(file_path)
            else:
                os.remove(file_path)
            return redirect('main_with_path', path=path)
        else:
            error_message = "Fichier introuvable."
            return render(request, 'main.html', {'error': error_message, 'path': path})
    return redirect('main')

def download_file(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        file_name = body.get('file_name')
        path = body.get('path', '')
        current_dir = os.path.join(base_dir, path)
        file_path = os.path.join(current_dir, file_name)
        if os.path.exists(file_path):
            file_url = request.build_absolute_uri(os.path.join('uploads', path, file_name))
            return JsonResponse({'url': file_url})
        else:
            return JsonResponse({'error': 'Fichier introuvable.'}, status=404)
    return JsonResponse({'error': "Méthode non autorisée."}, status=405)


def move_file(request):
    print('move')
    if request.method == 'POST':
        body = json.loads(request.body)
        file_name = body.get('file_name')
        folder_name = body.get('folder_name')
        path = body.get('path', '')
        print(file_name, folder_name, path)
        current_dir = os.path.join(base_dir, path)
        file_path = os.path.join(current_dir, file_name)
        new_folder_path = os.path.join(current_dir, folder_name)
        new_file_path = os.path.join(new_folder_path, file_name)
        print(file_path, new_folder_path, new_file_path)
        if os.path.exists(file_path) and os.path.exists(new_folder_path):
            if os.path.isdir(file_path):
                print("is dir")
                shutil.move(file_path, new_folder_path)
            else:
                shutil.move(file_path, new_file_path)
            return redirect('main_with_path', path=folder_name)
        else:
            error_message = "Fichier ou dossier introuvable."
            return render(request, 'main.html', {'error': error_message, 'path': path})
    return redirect('main')

def copy_file(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        file_name = body.get('file_name')
        path = body.get('path', '')
        if file_name[-1] != '/':
            file_name = file_name.split('/', 3)[-1]
        else:
            file_name = file_name[1:-1]
        file_path = os.path.join(base_dir, file_name)
        path=os.path.join(path, os.path.basename(file_name))
        

        if os.path.isdir(file_path):
            print('file_name', file_name, 'file_path', file_path, 'path', path)
            print("is dir")
            shutil.copytree(file_path, path, dirs_exist_ok=True)
        else:
            shutil.copy2(file_path, path)
        return redirect('main_with_path', path=path)
  
    return redirect('main')


def import_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        if uploaded_file.size > 40000000:
            return render(request, 'main.html', {'error': 'Le fichier est trop volumineux.'})

        path = request.POST.get('path', '')

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


        current_dir = os.path.join(base_dir, path)
        
        folder_path = os.path.join(current_dir, folder_name)
        
        if folder_name and not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return redirect('main_with_path', path=path)
        else:
            error_message = "Nom de dossier invalide ou dossier existe déjà."
            return render(request, 'main.html', {'error': error_message, 'path': path})

    return redirect('main')



@login_required
def my_view(request):
    # Récupérer le nom d'utilisateur de l'utilisateur connecté
    username = request.user.username
    return render(request, 'mon_template.html', {'username': username})

def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')