from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from scripts.models import ScriptComment


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(ScriptComment, id=comment_id)
    if comment.author == request.user:
        comment.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        return redirect(request.META.get("HTTP_REFERER", "/"))