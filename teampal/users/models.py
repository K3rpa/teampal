# users/models.py

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255)  
    avatar_url = models.URLField(null=True, blank=True)  

    def __str__(self):
        return self.content

class Friend(models.Model):
    user = models.OneToOneField(User, related_name="friend_list", on_delete=models.CASCADE, null=True, blank=True)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)

    def __str__(self):
        return self.user.username if self.user else "No User"

    @classmethod
    def make_friend(cls, user, new_friend):
        friend_list, created = cls.objects.get_or_create(user=user)
        friend_list.friends.add(new_friend)

    @classmethod
    def lose_friend(cls, user, new_friend):
        friend_list, _ = cls.objects.get_or_create(user=user)
        friend_list.friends.remove(new_friend)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"

class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    game = models.CharField(max_length=100)
    members_needed = models.IntegerField()
    contact = models.CharField(max_length=100)
    creator = models.CharField(max_length=255, null=True, blank=True)


class Trade(models.Model):
    game_name = models.CharField(max_length=255)
    item_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    status = models.CharField(max_length=3, choices=[('WTB', 'Want to Buy'), ('WTS', 'Want to Sell')])
    quantity = models.IntegerField()
    expected_price = models.FloatField()
    current_offer = models.FloatField()
    current_quantity = models.IntegerField(default=0)
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.item_name} ({self.status})"

class Offer(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='offers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    offer_price = models.FloatField()
    offer_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.offer_price} for {self.offer_quantity}"