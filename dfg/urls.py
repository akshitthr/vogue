from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signin", views.signin, name="signin"),
    path("signup", views.signup, name="signup"),
    path("signout", views.signout, name="signout"),
    path("discussions", views.all_discussions, name="discussions"),
    path("d/<int:discussion_id>", views.discussion, name="discussion"),
    path("new", views.new, name="new"),
    path("user/<str:username>", views.user, name="user"),
    path("follow", views.follow, name="follow"),
    path("join", views.join, name="join"),
    path("following", views.following, name="following"),
    path("like/<int:id>", views.like, name="like")
]
