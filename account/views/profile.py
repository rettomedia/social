from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import Post


@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user).order_by('-id')

    return render(request, 'account/profile.jinja', context={
        'user':request.user,
        'posts':posts,
    })