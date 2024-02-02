from django.shortcuts import get_object_or_404, redirect
from account.models import Comment
from django.contrib.auth.decorators import login_required

@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if comment.author == request.user:
        comment.delete()
        return redirect('profile')