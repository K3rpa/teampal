# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Friend
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import FriendRequest



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
    friend_requests = FriendRequest.objects.filter(to_user=user, is_active=True)

    query = request.GET.get('search', '')
    user_list = None
    if query:
        user_list = User.objects.filter(username__icontains=query).exclude(username=user.username)
    
    return render(request, 'chat/friend_list.html', {
        'friends': friends,
        'users': user_list,
        'query': query,
        'friend_requests': friend_requests
    })

def add_friend(request, username):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        user = request.user
        new_friend = User.objects.get(username=username)
        if user != new_friend:
            send_friend_request(request, username)
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


def send_friend_request(request, username):
    if request.user.is_authenticated:
        try:
            to_user = User.objects.get(username=username)
            if request.user != to_user:
                FriendRequest.objects.create(from_user=request.user, to_user=to_user)
                messages.success(request, f'Friend request sent to {username}.')
            else:
                messages.error(request, "You cannot send a friend request to yourself.")
        except User.DoesNotExist:
            messages.error(request, f"User {username} not found.")
    return redirect('friend_list')


def friend_requests(request):
    if request.user.is_authenticated:
        friend_requests = FriendRequest.objects.filter(to_user=request.user, is_active=True)
        return render(request, 'some_template.html', {'friend_requests': friend_requests})


def accept_friend_request(request, request_id):
    if request.user.is_authenticated:
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user, is_active=True)
            friend_request.is_active = False
            friend_request.save()
            Friend.make_friend(request.user, friend_request.from_user)
            messages.success(request, "Friend request accepted.")
        except FriendRequest.DoesNotExist:
            messages.error(request, "Friend request not found.")
    return redirect('friend_list')

def decline_friend_request(request, request_id):
    if request.user.is_authenticated:
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user, is_active=True)
            friend_request.is_active = False
            friend_request.save()
            messages.success(request, "Friend request declined.")
        except FriendRequest.DoesNotExist:
            messages.error(request, "Friend request not found.")
    return redirect('friend_list')

def general_chat(request):
    return render(request, 'chat/room2.html', {'room_name': 'general_chat'})


def trade(request):
    return render(request, 'chat/trade.html')

def tournament(request):
    return render(request, 'chat/tour.html')

def team_search(request):
    return render(request, 'chat/team_search.html')

def apex_general_chat(request):
    return render(request, 'chat/room2.html', {'room_name': 'apex_general_chat'})

def apex_trade(request):
    return render(request, 'chat/apex_trade.html')

def apex_team_search(request):
    return render(request, 'chat/apex_team_search.html')

def cs2_general_chat(request):
    return render(request, 'chat/room2.html', {'room_name': 'cs2_general_chat'})

def lol_general_chat(request):
    return render(request, 'chat/room2.html', {'room_name': 'lol_general_chat'})

def valorant_general_chat(request):
    return render(request, 'chat/room2.html', {'room_name': 'valorant_general_chat'})