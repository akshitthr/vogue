from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass


class Discussion(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    discussion = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    discussion = models.ForeignKey("Discussion", on_delete=models.CASCADE, blank=False)
    post = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class UserFollow(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")


class DiscussionFollow(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE)
    discussion = models.ForeignKey("Discussion", on_delete=models.CASCADE)


class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    liked_user = models.ForeignKey("User", on_delete=models.CASCADE)
