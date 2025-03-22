from django.shortcuts import redirect, get_object_or_404
from groups.models import Member, Group
from django.contrib.auth.decorators import login_required

@login_required
def join_group(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if not group.is_member(request.user):
        Member.objects.create(
            user=request.user,
            group=group
        )

        return redirect('group_index')
    else:
        return redirect('group_index')