from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("cs2/", views.cs2, name="cs2"),
    path("apex/", views.apex, name="apex"),
    path("lol/", views.lol, name="lol"),
    path("valorant/", views.valorant, name="valorant"),
    path('friend_list/', views.friend_list, name='friend_list'),
    path('add_friend/<str:username>/', views.add_friend, name='add_friend'),
    path('remove_friend/<str:username>/', views.remove_friend, name='remove_friend'),
    path('search_user/', views.search_user, name='search_user'),
    path('start_private_chat/<str:friend_username>/', views.start_private_chat, name='start_private_chat'),
    path('send_friend_request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('friend_requests/', views.friend_requests, name='friend_requests'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    #----------------dashboard---------------------------------
    path('dashboard/general_chat/', views.general_chat, name='dashboard.general_chat'),
    path('dashboard/team_search/', views.team_search, name='dashboard.team_search'),
    path('dashboard/trade/', views.trade, name='dashboard.trade'),
    path('dashboard/tournament/', views.tournament, name='dashboard.tournament'),
    path('chat/<str:room_name>/', views.room, name='room'),
    #----------------dashboard---------------------------------
    path('apex/apex_general_chat/', views.apex_general_chat, name='apex.apex_general_chat'),



]