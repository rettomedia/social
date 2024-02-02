from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from account.models import Post, Comment
from core.models import CustomUser
from core.forms import CommentForm
from django.urls import reverse


def post_detail(request, username, post_slug):
    user = get_object_or_404(CustomUser, username=username)
    post = get_object_or_404(Post, slug=post_slug)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post_detail', args=[username, post_slug]))
    else:
        form = CommentForm()

    return render(request, 'core/post-detail.jinja', context={
        'user':user,
        'post':post,
        'form':form,
        'comments':comments,
    })