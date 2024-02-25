from django.shortcuts import redirect, get_object_or_404
from posts.models import Like, Post
from django.contrib.auth.decorators import login_required


@login_required
def like_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    
    if Like.objects.filter(from_user=request.user, post=post).exists():
        return redirect('/')
    
    else:
        Like.objects.create(
            from_user=request.user,
            post=post
        )

        return redirect('/')