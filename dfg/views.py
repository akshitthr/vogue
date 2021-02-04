from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, Discussion, Post, Comment, UserFollow, Like, DiscussionFollow


# Index view
def index(request):

    # Check user authentication
    if request.user.is_authenticated:

        # Look if user has searched
        if request.GET.get("q"):
            # Get posts that the user searched for
            posts = Post.objects.filter(post__icontains=request.GET.get("q")).order_by("-timestamp").all()

        else:
            # Get all posts
            posts = Post.objects.all().order_by("-timestamp").all()
        
        comments = []

        # Iterate through posts
        for post in list(posts):
            post_comments = Comment.objects.filter(post=post.id).order_by("-timestamp").all()

            # Iterate through comments
            for comment in post_comments:
                comments.append(comment)
        
        # Pagination
        paginator = Paginator(posts, 10)
        page = request.GET.get("page", 1)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        return render(request, "vogue/index.html", {
            "posts": posts,
            "comments": comments
        })

    else:
        return render(request, "vogue/welcome.html")


# Sign in view
def signin(request):

    # Check request method
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))

        # Attempt to lo user in
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "vogue/signin.html", {
                "message": "Invalid username and/or password"
            })

    else:
        return render(request, "vogue/signin.html")


# Sign out view
def signout(request):

    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Sign up view
def signup(request):

    # Check request method
    if request.method == "POST":
        
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        email  = request.POST.get("email")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")

        # Check if passwords match
        if password != confirm:
            return render(request, "vogue/signup.html", {
                "message": "Passwords must match"
            })
        
        # Password length must be at least 8
        elif len(password) < 8:
            return render(request, "vogue/signup.html", {
                "message": "Password must be at least 8 characters long"
            })
        
        # Attempt to create user
        try:
            user = User.objects.create_user(username, email, password, first_name=fname, last_name=lname)
            user.save()
        
        # User picks unavailable username
        except IntegrityError:
            return render(request, "vogue/signup.html", {
                "message": "Username already taken"
            })
        
        # Log user in
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "vogue/signup.html")


# All discussions view
@login_required(login_url='/signin')
def all_discussions(request):

    # Check request method
    if request.method == "POST":
        
        # Create new discussion
        if request.POST.get("name"):
            discussion = Discussion(user=request.user, discussion=request.POST.get("name"))
            discussion.save()
            return HttpResponseRedirect(reverse("discussion", kwargs={"discussion_id": discussion.id}))
        
        # Return error if field is empty
        else:
            return render(request, "vogue/error.html", {
                "code": 400,
                "message": "Field/s cannot be empty"
            })

    else:    
        return render(request, "vogue/discussions.html", {
            "discussions": Discussion.objects.all()
        })


# Discussion view
@login_required(login_url='/signin')
def discussion(request, discussion_id):

    try:
        discussion = Discussion.objects.get(id=discussion_id)
    
    except Discussion.DoesNotExist:
        return render(request, "vogue/error.html", {
            "code": 404,
            "message": "Requested page not found"
        })
    
    # Get all posts from discussion
    posts = Post.objects.filter(discussion=discussion_id).order_by("-timestamp").all()
    comments = []

    # Iterate through posts
    for post in list(posts):
        post_comments = Comment.objects.filter(post=post.id).order_by("-timestamp").all()

        # Iterate through comments
        for comment in post_comments:
            comments.append(comment)
    
    # Paginate
    paginator = Paginator(posts, 10)
    page = request.GET.get("page", 1)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Check if user is following discussion
    try:
        DiscussionFollow.objects.get(follower=request.user, discussion=discussion)
        member = True
    
    except DiscussionFollow.DoesNotExist:
        member = False
    
    return render(request, "vogue/discussion.html", {
        "discussion": discussion,
        "posts": posts,
        "comments": comments,
        "member": member
    })


# Create posts/comments
@login_required(login_url='/signin')
def new(request):

    # Request method must be post
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))

    # Create new post
    if request.POST.get("content"):
        post = Post(user=request.user, discussion=Discussion.objects.get(id=request.POST.get("discussion_id")), post=request.POST.get("content"))
        post.save()
    
    # Create new comment
    elif request.POST.get("comment"):
        comment = Comment(user=request.user, post=Post.objects.get(id=request.POST.get("post_id")), comment=request.POST.get("comment"))
        comment.save()
    
    # Return error if input field is empty
    else:
        return render(request, "vogue/error.html", {
            "code": 400,
            "message": "Field/s cannot be empty"
        })
    
    # Find page to redirect user to
    page_name = request.POST.get("pagename")
    if page_name == "discussion":
        return HttpResponseRedirect(reverse("discussion", kwargs={
            "discussion_id": request.POST.get("discussion_id")
        }))
    
    elif page_name == "user":
        return HttpResponseRedirect(reverse("user", kwargs={
            "username": request.POST.get("username")
        }))
    
    else:
        return HttpResponseRedirect(reverse(page_name))


# User profile view
@login_required(login_url='/signin')
def user(request, username):

    try:
        user = User.objects.get(username=username)
    except:
        return render(request, "vogue/error.html", {
            "code": 404,
            "message": "Requested page not found"
        })
    
    # Get all user's posts
    posts = Post.objects.filter(user=user).order_by("-timestamp").all()
    comments = []

    # Iterate through posts
    for post in list(posts):
        post_comments = Comment.objects.filter(post=post.id).order_by("-timestamp").all()

        # Itertae through comments
        for comment in post_comments:
            comments.append(comment)
    
    # Pagination
    paginator = Paginator(posts, 10)
    page = request.GET.get("page", 1)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Check if current user follows displayed user
    try:
        UserFollow.objects.get(follower=request.user, following=user)
        following = True
    except:
        following = False
    
    return render(request, "vogue/user.html", {
        "userinfo": user,
        "posts": posts,
        "comments": comments,
        "following": following,
        "following_count": UserFollow.objects.filter(follower=user).count(),
        "follower_count": UserFollow.objects.filter(following=user).count()
    })


# Follow/Unfollow users
@login_required(login_url='/signin')
def follow(request):

    # Request method must be post
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("index"))
    
    try:
        UserFollow.objects.get(follower=request.user, following=User.objects.get(username=request.POST.get("username"))).delete()
    
    except UserFollow.DoesNotExist:
        follow = UserFollow(follower=request.user, following=User.objects.get(username=request.POST.get("username")))
        follow.save()
    
    return HttpResponseRedirect(reverse("user", kwargs={"username": request.POST.get("username")}))


# Follow/Unfollow discussions
@login_required(login_url='/signin')
def join(request):

    # Request method must be post
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("index"))
    
    discussion_id = request.POST.get("discussion")
    
    try:
        DiscussionFollow.objects.get(follower=request.user, discussion=Discussion.objects.get(id=discussion_id)).delete()
    
    except DiscussionFollow.DoesNotExist:
        follow = DiscussionFollow(follower=request.user, discussion=Discussion.objects.get(id=discussion_id))
        follow.save()
    
    return HttpResponseRedirect(reverse("discussion", kwargs={"discussion_id": discussion_id}))


# Following View
@login_required(login_url='/signin')
def following(request):

    # Get all posts
    following_list = list(UserFollow.objects.filter(follower=request.user))
    discussions_list = list(DiscussionFollow.objects.filter(follower=request.user))
    posts = []
    
    # Get posts from people the user follows
    for follow in following_list:
        if request.GET.get("q"):
            user_posts = Post.objects.filter(user=User.objects.get(username=follow.following)).filter(post__icontains=request.GET.get("q"))

        else:
            user_posts = Post.objects.filter(user=User.objects.get(username=follow.following))
        
        for post in user_posts:
            posts.append(post)
    
    # Get posts from discussions the user follows
    for discussion in discussions_list:
        if request.GET.get("q"):
            discussion_posts = Post.objects.filter(discussion=discussion.discussion).filter(post__icontains=request.GET.get("q"))

        else:
            discussion_posts = Post.objects.filter(discussion=discussion.discussion)
        
        posts += [post for post in discussion_posts if post not in posts]

    # Sort posts
    posts.sort(key=lambda x: x.timestamp, reverse=True)
    comments = []

    # Get comments for posts
    for post in posts:
        post_comments = Comment.objects.filter(post=post.id).order_by("-timestamp").all()

        for comment in post_comments:
            comments.append(comment)
    
    # Pagination
    paginator = Paginator(posts, 10)
    page = request.GET.get("page", 1)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, "vogue/following.html", {
        "posts": posts,
        "comments": comments
    })


# Like/Unlike post
@csrf_exempt
@login_required(login_url='/signin')
def like(request, id):
    
    # Check request method
    if request.method == "GET":

        # Get like count
        try:
            count = Like.objects.filter(post=id).count()
        except Like.DoesNotExist:
            count = 0
        
        # Check if user has liked post
        try:
            Like.objects.get(post=id, liked_user=request.user)
            user_liked = True
        except:
            user_liked = False
        
        return JsonResponse({"count": count, "user_liked": user_liked})

    else:

        try:
            Like.objects.get(post=id, liked_user=request.user).delete()
        
        except Like.DoesNotExist:
            liked_user = Like(post=Post.objects.get(id=id), liked_user=request.user)
            liked_user.save()
        
        return JsonResponse(204, safe=False)
