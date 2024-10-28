from django.urls import path
from . import views


urlpatterns = [
    path("", views.main, name="main"),
    path("main/", views.main, name="main"),
    path("home/",views.home, name="home"),
    path("login/", views.login, name='login'),
    path("profile/", views.profile, name='profile'),
]