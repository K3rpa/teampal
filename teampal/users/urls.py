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
    path('apex/team_search/', views.apex_team_search, name='apex.team_search'),
    path('dashboard/tournament/', views.tournament, name='dashboard.tournament'),
    path('apex/trade/', views.apex_trade, name='apex.trade'),
    #path('apex/tournament/', views.apex_tournament, name='apex.tournament'),
    #-----------------apex end---------------------------------
    path('cs2/cs2_general_chat/', views.cs2_general_chat, name='cs2_general_chat'),
    path('cs2/team_search/', views.cs2_team_search, name='cs2.team_search'),
    path('cs2/trade/', views.cs2_trade, name='cs2.trade'),
    path('dashboard/tournament/', views.tournament, name='dashboard.tournament'),
    #path('cs2/tournament/', views.cs2_tournament, name='cs2.tournament'),
    #------------------cs2 end----------------------------------    
    path('lol/lol_general_chat/', views.lol_general_chat, name='lol_general_chat'),
    path('lol/team_search/', views.lol_team_search, name='lol.team_search'),
    path('lol/trade/', views.lol_trade, name='lol.trade'),
    path('dashboard/tournament/', views.tournament, name='dashboard.tournament'),
    #path('lol/tournament/', views.lol_tournament, name='lol.tournament'),
    #-------------------lol end-----------------------------------
    path('valorant/valorant_general_chat/', views.valorant_general_chat, name='valorant_general_chat'),
    path('valorant/team_search/', views.valorant_team_search, name='valorant.team_search'),
    path('valorant/trade/', views.valorant_trade, name='valorant.trade'),
    path('dashboard/tournament/', views.tournament, name='dashboard.tournament'),
   # path('valorant/tournament/', views.valorant_tournament, name='valorant.tournament'),
    #-------------------valorant end------------------------------




]