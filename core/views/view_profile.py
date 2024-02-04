from django.shortcuts import render, get_object_or_404, redirect
from core.models import CustomUser
from account.models import Post, Comment
from account.models import FriendRequest
from django.db.models import Q

def view_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts = Post.objects.filter(author=user)
    comments = Comment.objects.filter(author=user)
    if user != request.user:
        if request.user.is_authenticated:
            friend_request_sent = FriendRequest.objects.filter(from_user=request.user, to_user=user, is_accepted=False).exists()
            is_friend = FriendRequest.objects.filter(Q(from_user=request.user, to_user=user), is_accepted=True)

        return render(request, 'core/view-profile.jinja', context={
            'user':user,
            'posts':posts,
            'comments':comments,
            'is_friend':is_friend,
            'friend_request_sent':friend_request_sent,
        })
    else:
        return redirect('profile')