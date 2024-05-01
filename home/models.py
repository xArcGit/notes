import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=60, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


class Notes(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    shareid = models.CharField(max_length=36, unique=True)

    def save(self, *args, **kwargs):
        if not self.shareid:
            self.shareid = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} {self.content} {self.shareid}"
