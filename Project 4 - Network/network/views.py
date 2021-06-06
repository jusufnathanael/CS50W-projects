import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator

from .models import *


def index(request):
    posts = Post.objects.annotate(likes=Count('like')).order_by('-timestamp')
    paginator = Paginator(posts, 10) # show 10 posts per page
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    page_object = paginator.get_page(page_number)
    if not request.user.is_authenticated:
        return render(request, "network/index.html", {
        "posts": page_object, "action": "", "profile_bool": False,
        "num_pages": range(paginator.num_pages), "current_page": int(page_number)
    })
    likes = []
    for like in Like.objects.filter(user=request.user):
        likes += [like.post]
    return render(request, "network/index.html", {
        "posts": page_object, "likes": likes, "action": "","profile_bool": False,
        "num_pages": range(paginator.num_pages), "current_page": int(page_number)
    })


@login_required
def add_or_edit(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    if data.get("action") == 'add':
        p = Post.objects.create(user=request.user, details=data.get("details"))
        p.save()
        return JsonResponse({"message": "Post posted successfully."}, status=201)
    else:
        p = Post.objects.filter(id=data.get("post_id"))
        p.update(details=data.get("details"))
        return JsonResponse({"message": "Post updated successfully"}, status=201)


def profile(request, name):

    user = User.objects.get(username=name)
    followed = False
    likes = []
    if request.user.is_authenticated:
        followed = Follow.objects.filter(follows=request.user, followed=user).exists()
        for like in Like.objects.filter(user=request.user):
            likes += [like.post]
    
    # get posts and paginate
    posts = Post.objects.filter(user=user).annotate(likes=Count('like')).order_by('-timestamp')
    paginator = Paginator(posts, 10) # show 10 posts per page
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    page_object = paginator.get_page(page_number)

    # Return the profile contents
    if request.method == "GET":
        return render(request, "network/index.html", {
            "me": request.user, "user": user, "followed": followed, "action": f"/profile/{name}",
            "followers": Follow.objects.filter(followed=user).count(),
            "following": Follow.objects.filter(follows=user).count(),
            "posts": page_object, "ilkes": likes, "profile_bool": True,
            "num_pages": range(paginator.num_pages), "current_page": int(page_number)
        })

    # Follow a person
    if request.method == "PUT":
        if followed:
            Follow.objects.get(follows=request.user, followed=user).delete()
            return JsonResponse({"message": f"{user.username} unfollowed."}, status=200)
        else:
            f = Follow.objects.create(follows=request.user, followed=user)
            f.save()
            return JsonResponse({"message": f"{user.username} followed."}, status=200)


@login_required
def following(request):
    # get following users
    followed = Follow.objects.filter(follows=request.user).select_related('followed').distinct()
    usernames = []
    for user in followed:
        usernames += [user.followed]
    # get posts and paginate
    posts = Post.objects.filter(user__in=usernames).annotate(likes=Count('like')).order_by('-timestamp')
    paginator = Paginator(posts, 10) # show 10 posts per page
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    page_object = paginator.get_page(page_number)
    # get liked posts
    likes = []
    for like in Like.objects.filter(user=request.user):
        likes += [like.post]
    return render(request, "network/index.html", {
        "posts": page_object, "likes": likes, "action": "following", "profile_bool": False,
        "num_pages": range(paginator.num_pages), "current_page": int(page_number)
    })


@login_required
def like(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    post = Post.objects.get(id=id)
    liked = Like.objects.filter(user=request.user, post=post).exists()

    if not liked:
        Like.objects.create(user=request.user, post=post).save()
        return JsonResponse({"message": f"{post} liked."}, status=200)
    else:
        Like.objects.get(user=request.user, post=post).delete()
        return JsonResponse({"message": f"{post} unliked."}, status=200)


def login_view(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
