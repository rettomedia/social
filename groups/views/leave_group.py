from django.shortcuts import redirect, get_object_or_404
from groups.models import Member, Group
from django.contrib.auth.decorators import login_required

@login_required
def leave_group(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if group.is_member(request.user):
        Member.objects.filter(user=request.user, group=group).delete()
        return redirect('group_index')
    else:
        return redirect('group_index')