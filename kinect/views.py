from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator

from .models import User, NewPost


def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:

        #Show 10 posts at a time
        post= NewPost.objects.all()
        paginator= Paginator(post,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "page_obj": page_obj,
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))
    
def profile(request, user):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=user)
        posts= NewPost.objects.filter(user=user)
        paginator=Paginator(posts,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    else:
        HttpResponseRedirect(reverse('login'))

    return render(request, "network/profile.html", {
        "page_obj": page_obj,
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
    
def following(request):
    user= request.user
    if user.is_authenticated:
        posts = NewPost.objects.filter(user__in=user.following.all())
        paginator=Paginator(posts,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, "network/following.html", {
            "page_obj":page_obj
        })


@login_required 
@csrf_exempt
def post(request, post_id):

    try:
        post= NewPost.objects.get(user=request.user, pk=post_id)
    except NewPost.DoesNotExist:
        return JsonResponse('Post Does Not Exist', status=404)
    
    if request.method == 'GET':
        return JsonResponse(post.serialize())
    elif request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('body') is not None:
            post.body = data['body']
        post.save()
        likes= post.like.count()
        user_liked = request.user in post.like.all()
        return JsonResponse({'user': str(post.user), 'body': post.body, 'likes':likes, 'liked': user_liked} )
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
    
@csrf_exempt 
def like(request, post_id):
    post= NewPost.objects.get(pk=post_id)

    if request.method == 'POST':
        if request.user not in post.like.all():
            post.like.add(request.user)
            liked=True
        else:
            post.like.remove(request.user)
            liked=False
        post.save()
        likeCount= post.like.count()

        return JsonResponse({'likes': likeCount, 'liked': liked})
        
        

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
        return JsonResponse({"message": "Post Submitted."}, status=201)

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
