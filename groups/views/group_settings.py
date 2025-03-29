from django.shortcuts import render, get_object_or_404, redirect
from groups.forms import GroupForm
from groups.models import Group
from django.contrib.auth.decorators import login_required

@login_required
def group_settings(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if group.owned_by == request.user:
        if request.method == 'POST':
            form = GroupForm(request.POST, instance=group)
            if form.is_valid():
                form.save()
                return redirect('group_index')
            else:
                return redirect('group_index')
        else:
            form = GroupForm(instance=group)
        return render(request, 'groups/group-settings.jinja', context={
            'form':form
        })
    else:
        return redirect('group_index')