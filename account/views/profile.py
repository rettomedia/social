from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import Post, Comment
from account.models import FriendRequest
from django.db.models import Q

@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)
    comments = Comment.objects.filter(author=request.user)
    sent_requests = FriendRequest.objects.filter(from_user=request.user, is_accepted=True)
    received_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=True)
    
    friends = (sent_requests | received_requests).distinct()
    return render(request, 'account/profile.jinja', context={
        'posts':posts,
        'comments':comments,
        'friends':friends,
    })