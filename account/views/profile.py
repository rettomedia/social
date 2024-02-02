from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import Post, Comment

@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)
    comments = Comment.objects.filter(author=request.user)
    return render(request, 'account/profile.jinja', context={
        'posts':posts,
        'comments':comments,
    })