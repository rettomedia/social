from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from groups.models import Group


@login_required
def delete_group(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)

    if group.owned_by == request.user:
        group.delete()
        return redirect('group_index')
    else:
        return redirect(request.META.get("HTTP_REFERER", "/"))