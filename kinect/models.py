from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class NewPost(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    body = models.TextField(blank=True)
    Timestamp= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}, {self.Timestamp}"