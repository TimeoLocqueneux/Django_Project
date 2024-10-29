from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("main/", views.main, name="main"),
    path("home/",views.home, name="home"),
    path("login/", views.login, name='login'),
    path("profile/", views.profile, name='profile'),
    path('success/', views.success_view, name='success'),
    path('register/', views.register_view, name='register'),
    path('login_view/', views.login_view, name='login'),
]