from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .models import User, NewPost


def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        post= NewPost.objects.all()
        return render(request, "network/index.html", {
            "post": post
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))
    
def profile(request, user):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=user)
        posts= NewPost.objects.filter(user=user)
    else:
        HttpResponseRedirect(reverse('login'))

    return render(request, "network/profile.html", {
        "posts": posts,
        "user": user
    })

@login_required 
@csrf_exempt 
def follow(request, user):

    if request.method == 'POST':
        #get user
        user_to_follow = get_object_or_404(User, username=user)

        #unfollow the user profile
        if request.user in user_to_follow.follower.all():
            # If so, unfollow
            user_to_follow.follower.remove(request.user)
            request.user.following.remove(user_to_follow)
            followed = False
        else:
            #follow the user profile
            user_to_follow.follower.add(request.user)
            request.user.following.add(user_to_follow)
            followed=True

        #save the info
        user_to_follow.save()
        request.user.save()

        followers_count = user_to_follow.follower.count()

        #return JSON response
        return JsonResponse({'followed': followed, 'followers': followers_count})

@csrf_exempt  
@login_required 
def new_post(request):

    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        body = data.get("body", "")

        post = NewPost(
            user=user,
            body=body
        )
        post.save()
        return JsonResponse({"message": "Email sent successfully."}, status=201)

def login_view(request):
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
