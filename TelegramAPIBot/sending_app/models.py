from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):
    token = models.CharField(256, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_user = models.OneToOneField('TelegramUser', on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.token


class TelegramUser(models.Model):
    user_id = models.CharField(max_length=256)
    chat_id = models.CharField(max_length=256)

    def __str__(self):
        return str(self.user_id)


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    send_time = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return str(self.owner) + f': {self.send_time}'
