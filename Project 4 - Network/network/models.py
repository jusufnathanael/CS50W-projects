from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} posted by {self.user} on {self.timestamp}"


class Follow(models.Model):
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
    timestamp = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.follows} follows {self.followed}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    post = models.ForeignKey(Post, on_delete=CASCADE)
    timestamp = models.DateTimeField(default=datetime.now())

    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f"{self.user} like post {self.post.id} by {self.post.user}"
