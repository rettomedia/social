from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from groups.models import Group, Member, GroupPost


@login_required
def group(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    posts = GroupPost.objects.filter(group=group)

    if group.is_public:
        members = Member.objects.filter(group=group).values_list('user', flat=True)

        return render(request, 'groups/group.jinja', {
            'group':group,
            'members':members,
            'posts':posts
        })
    else:
        member = get_object_or_404(Member, user=request.user, group=group)
        members = Member.objects.filter(group=group).values_list('user', flat=True)

        if member:
            return render(request, 'groups/group.jinja', {
                'group':group,
                'members':members,
                'posts':posts,
            })
        else:
            return redirect('group_index')