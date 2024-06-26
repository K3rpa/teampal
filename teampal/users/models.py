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


############################################################################################################
class Apex_Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    game = models.CharField(max_length=100)
    members_needed = models.IntegerField()
    contact = models.CharField(max_length=100)
    creator = models.CharField(max_length=255, null=True, blank=True)

class apex_Trade(models.Model):
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

class apex_Offer(models.Model):
    trade = models.ForeignKey(apex_Trade, on_delete=models.CASCADE, related_name='offers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    offer_price = models.FloatField()
    offer_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.offer_price} for {self.offer_quantity}"


class apex_TournamentPost(models.Model):
    name = models.CharField(max_length=255)
    game = models.CharField(max_length=255, null=True)
    date = models.DateField()
    description = models.TextField()
    team_count = models.IntegerField()
    prize = models.CharField(max_length=100)
    interest_count = models.IntegerField(default=0)
    website = models.URLField(blank=True, null=True)
    contact = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class apex_TournamentInterest(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tournament = models.ForeignKey(apex_TournamentPost, on_delete=models.CASCADE)
    is_interested = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'tournament')
############################################################################################################

class cs2_Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    game = models.CharField(max_length=100)
    members_needed = models.IntegerField()
    contact = models.CharField(max_length=100)
    creator = models.CharField(max_length=255, null=True, blank=True)

class cs2_Trade(models.Model):
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

class cs2_Offer(models.Model):
    trade = models.ForeignKey(cs2_Trade, on_delete=models.CASCADE, related_name='offers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    offer_price = models.FloatField()
    offer_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.offer_price} for {self.offer_quantity}"

class cs2_TournamentPost(models.Model):
    name = models.CharField(max_length=255)
    game = models.CharField(max_length=255, null=True)
    date = models.DateField()
    description = models.TextField()
    team_count = models.IntegerField()
    prize = models.CharField(max_length=100)
    interest_count = models.IntegerField(default=0)
    website = models.URLField(blank=True, null=True)
    contact = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class cs2_TournamentInterest(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tournament = models.ForeignKey(cs2_TournamentPost, on_delete=models.CASCADE)
    is_interested = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'tournament')
############################################################################################################

class lol_Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    game = models.CharField(max_length=100)
    members_needed = models.IntegerField()
    contact = models.CharField(max_length=100)
    creator = models.CharField(max_length=255, null=True, blank=True)

class lol_Trade(models.Model):
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

class lol_Offer(models.Model):
    trade = models.ForeignKey(lol_Trade, on_delete=models.CASCADE, related_name='offers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    offer_price = models.FloatField()
    offer_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.offer_price} for {self.offer_quantity}"

class lol_TournamentPost(models.Model):
    name = models.CharField(max_length=255)
    game = models.CharField(max_length=255, null=True)
    date = models.DateField()
    description = models.TextField()
    team_count = models.IntegerField()
    prize = models.CharField(max_length=100)
    interest_count = models.IntegerField(default=0)
    website = models.URLField(blank=True, null=True)
    contact = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class lol_TournamentInterest(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tournament = models.ForeignKey(lol_TournamentPost, on_delete=models.CASCADE)
    is_interested = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'tournament')
############################################################################################################
class valorant_Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    game = models.CharField(max_length=100)
    members_needed = models.IntegerField()
    contact = models.CharField(max_length=100)
    creator = models.CharField(max_length=255, null=True, blank=True)

class valorant_Trade(models.Model):
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

class valorant_Offer(models.Model):
    trade = models.ForeignKey(valorant_Trade, on_delete=models.CASCADE, related_name='offers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    offer_price = models.FloatField()
    offer_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.offer_price} for {self.offer_quantity}"

class valorant_TournamentPost(models.Model):
    name = models.CharField(max_length=255)
    game = models.CharField(max_length=255, null=True)
    date = models.DateField()
    description = models.TextField()
    team_count = models.IntegerField()
    prize = models.CharField(max_length=100)
    interest_count = models.IntegerField(default=0)
    website = models.URLField(blank=True, null=True)
    contact = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class valorant_TournamentInterest(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tournament = models.ForeignKey(valorant_TournamentPost, on_delete=models.CASCADE)
    is_interested = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'tournament')
############################################################################################################

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

class TournamentPost(models.Model):
    name = models.CharField(max_length=255)
    game = models.CharField(max_length=255, null=True)
    date = models.DateField()
    description = models.TextField()
    team_count = models.IntegerField()
    prize = models.CharField(max_length=100)
    interest_count = models.IntegerField(default=0)
    website = models.URLField(blank=True, null=True)
    contact = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TournamentInterest(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tournament = models.ForeignKey(TournamentPost, on_delete=models.CASCADE)
    is_interested = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'tournament')