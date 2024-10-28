from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('success/', views.success_view, name='success'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
]