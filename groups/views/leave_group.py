from django.shortcuts import redirect, get_object_or_404
from groups.models import Member, Group, GroupPost
from django.contrib.auth.decorators import login_required

@login_required
def leave_group(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if group.is_member(request.user):
        member = Member.objects.filter(user=request.user, group=group)
        member_posts = GroupPost.objects.filter(author=request.user, group=group)

        member.delete()
        member_posts.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        return redirect(request.META.get("HTTP_REFERER", "/"))