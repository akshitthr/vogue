from django.contrib import admin

from .models import User, Discussion, Post, Comment, UserFollow, DiscussionFollow, Like

# Register your models here.
admin.site.register(User)
admin.site.register(Discussion)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserFollow)
admin.site.register(DiscussionFollow)
admin.site.register(Like)
