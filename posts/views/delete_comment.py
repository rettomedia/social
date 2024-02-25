from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Comment
from django.urls import reverse


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        post = comment.post
        comment.delete()

        return HttpResponseRedirect(reverse('post_detail', args=[post.author.username,post.slug]))