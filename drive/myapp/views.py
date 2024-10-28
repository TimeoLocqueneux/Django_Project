from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def main(request):
    return render(request, "main.html")

def profile(request):
    return render(request, "profile.html")
