from django.shortcuts import redirect, get_object_or_404
from posts.models import Like, Post
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



@login_required
@csrf_exempt
def like_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    
    if Like.objects.filter(from_user=request.user, post=post).exists():
        Like.objects.filter(from_user=request.user, post=post).delete()
        likes_count = post.likes.count()
        return JsonResponse({'message': 'Post unliked successfully.', 'likes_count': likes_count})
    
    else:
        Like.objects.create(
            from_user=request.user,
            post=post
        )

        likes_count = post.likes.count()
        return JsonResponse({'message': 'Post liked successfully.', 'likes_count': likes_count})