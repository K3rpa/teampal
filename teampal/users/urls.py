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
    path("chat/", views.chat, name="chat"),
    path('chat/<str:room_name>/', views.room, name='room')
]