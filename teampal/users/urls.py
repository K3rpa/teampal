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


]