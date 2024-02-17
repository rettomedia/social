from django.shortcuts import render, get_object_or_404
from network.models import CustomUser
from posts.models import Post


def view_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts = Post.objects.filter(author=user)
    if user != request.user:

        return render(request, 'network/user-profile.jinja', context={
            'user':user,
            'posts':posts,
        })
    else:
        pass