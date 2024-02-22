from django.shortcuts import render
from account.models import Friend
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def settings(request):
    notifications = Friend.objects.filter(
        Q(from_user=request.user) |
        Q(to_user=request.user), is_accepted=False
    )

    return render(request, 'account/settings.jinja', context={
        'notifications':notifications,
    })