from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255)  # 标识消息属于哪个聊天室
    avatar_url = models.URLField(null=True, blank=True)  # 用户头像的 URL

    def __str__(self):
        return self.content