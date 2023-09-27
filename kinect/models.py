from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following= models.ManyToManyField('self',symmetrical=False, related_name="user_following")
    follower= models.ManyToManyField('self',symmetrical=False, related_name="user_followers")
    def __str__(self):
        return f"{self.username}"

class NewPost(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    body = models.TextField(blank=True)
    Timestamp= models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField('User',symmetrical=False, related_name="like_post")

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'body': self.body,
            'timestamp': self.Timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'likes': self.like.count()
        }