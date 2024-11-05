from django.urls import path
from . import views


urlpatterns = [
    path("", views.login_register_view, name="login_register"),
    path('login/', views.login_register_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path("main/", views.main, name="main"),
    path("profile/", views.profile, name='profile'),
    path('import-file/', views.import_file, name='import_file'),
    path('create-folder/', views.create_folder, name='create_folder'),
    path('rename-file/', views.rename_file, name='rename_file'),
    path('delete-file/', views.delete_file, name='delete_file'),
    path('download-file/', views.download_file, name='download_file'),
    path('<path:path>/', views.main, name='main_with_path'),
    ]
