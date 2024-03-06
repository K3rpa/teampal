from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Friend
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


User = get_user_model()

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

def chat(request):
    if request.user.is_authenticated:
        return redirect('friend_list')
    else:
        return redirect("login.html") 

def room(request, room_name):
    if request.user.is_authenticated:
        return render(request, 'chat/room.html', {
            'room_name': room_name
        })
    else:
        return redirect("login.html")
        
def start_private_chat(request, friend_username):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    
    try:
        friend = User.objects.get(username=friend_username)
        friend_list_instance = Friend.objects.filter(user=user).first()
        if friend_list_instance and friend in friend_list_instance.friends.all():
            chat_identifier = "_".join(sorted([user.username, friend_username]))
            return render(request, 'chat/room.html', {
                'room_name': chat_identifier
            })
        else:
            return redirect('friend_list')
    except User.DoesNotExist:
        return redirect('friend_list')



def search_user(request):
    if request.method == "GET":
        query = request.GET.get('username', '')
        user_list = User.objects.filter(username__icontains=query).exclude(username=request.user.username)
        url = f"{reverse('friend_list')}?search={query}"
        return HttpResponseRedirect(url)


def friend_list(request):
    user = request.user
    friend_list_instance = Friend.objects.filter(user=user).first()
    friends = friend_list_instance.friends.all() if friend_list_instance else User.objects.none()

    query = request.GET.get('search', '')
    user_list = None
    if query:
        user_list = User.objects.filter(username__icontains=query).exclude(username=user.username)
    
    return render(request, 'users/friend_list.html', {
        'friends': friends,
        'users': user_list,
        'query': query
    })

def add_friend(request, username):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        user = request.user
        new_friend = User.objects.get(username=username)
        if user != new_friend:
            Friend.make_friend(user, new_friend)
            messages.success(request, f'{new_friend.username} has been added as a friend.')
        else:
            messages.error(request, "You cannot add yourself as a friend.")
    except User.DoesNotExist:
        messages.error(request, "The requested user does not exist.")

    return HttpResponseRedirect(reverse('friend_list'))

def remove_friend(request, username):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        user = request.user
        old_friend = User.objects.get(username=username)
        Friend.lose_friend(user, old_friend)
        messages.success(request, f'{old_friend.username} has been removed from friends.')
    except User.DoesNotExist:
        messages.error(request, "The requested user does not exist.")

    return HttpResponseRedirect(reverse('friend_list'))