from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from posts.models import Post, Comment, Like
from network.models import CustomUser
from django.urls import reverse


def post_detail(request, username, post_slug):
    author = get_object_or_404(CustomUser, username=username)
    post = get_object_or_404(Post, slug=post_slug, author=author)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        Comment.objects.create(
            author=request.user,
            message=comment,
            post=post
        )

        return HttpResponseRedirect(reverse('post_detail', args=[author.username,post.slug]))


    user_liked_posts = set(Like.objects.filter(from_user=request.user).values_list('post_id', flat=True))
    return render(request, 'posts/post-detail.jinja', context={
        'post':post,
        'comments':comments,
        'user_liked_posts':user_liked_posts,
    })