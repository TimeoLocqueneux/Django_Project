from django.urls import path
from . import views


urlpatterns = [
    path("", views.login_register_view, name="login_register"),
    path("main/", views.main, name="main"),
    path("profile/", views.profile, name='profile'),
    path('import-file/', views.import_file, name='import_file'),
    path('create-folder/', views.create_folder, name='create_folder'),
    path('<path:path>/', views.main, name='main_with_path'),
    ]