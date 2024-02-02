from django.shortcuts import render, get_object_or_404, redirect
from core.models import CustomUser
from account.models import Post, Comment

def view_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts = Post.objects.filter(author=user)
    comments = Comment.objects.filter(author=user)
    if user != request.user:
        return render(request, 'core/view-profile.jinja', context={
            'user':user,
            'posts':posts,
            'comments':comments,
        })
    else:
        return redirect('profile')