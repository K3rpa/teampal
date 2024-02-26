from django.shortcuts import render, redirect
from django.contrib.auth import logout

def home(request):
    return render(request,"login.html")


def logout_view(request):
    logout(request)
    return redirect("/")


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html")
    else:
        return redirect("login.html")  

def cs2(request):
    if request.user.is_authenticated:
        return render(request, "cs2.html")
    else:
        return redirect("login.html")  

def apex(request):
    if request.user.is_authenticated:
        return render(request, "apex.html")
    else:
        return redirect("login.html")  

def lol(request):
    if request.user.is_authenticated:
        return render(request, "lol.html")
    else:
        return redirect("login.html")  

def valorant(request):
    if request.user.is_authenticated:
        return render(request, "valorant.html")
    else:
        return redirect("login.html")  