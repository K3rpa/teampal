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

