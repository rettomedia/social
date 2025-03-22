from django.shortcuts import render, get_object_or_404, redirect
from network.models import CustomUser
from posts.models import Post
from account.models import Friend
from django.db.models import Q



def view_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts = Post.objects.filter(author=user)
    if user.is_authenticated:
        if user != request.user:
            friend_request_sent = Friend.objects.filter(from_user=request.user, to_user=user, is_accepted=False).exists()
            is_friend = Friend.objects.filter((Q(from_user=request.user, to_user=user) | Q(from_user=user, to_user=request.user)), is_accepted=True).exists()


            return render(request, 'network/user-profile.jinja', context={
                'user':user,
                'posts':posts,
                'friend_request_sent': friend_request_sent,
                'is_friend': is_friend,
            })
        else:
            return redirect('profile')
    else:
        return redirect('index')