from django.shortcuts import render
from account.models import Friend
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def friend_list(request):
    friend_list = Friend.objects.filter(
        Q(from_user=request.user) |
        Q(to_user=request.user), is_accepted=True
    )

    friend_requests = Friend.objects.filter(
        Q(from_user=request.user) |
        Q(to_user=request.user), is_accepted=False
    )

    search = request.GET.get('search')
    if search:
        friend_list = friend_list.filter(
            Q(from_user__username__contains=search) |
            Q(to_user__username__contains=search)
        ).distinct()

    return render(request, 'account/friend-list.jinja', context={
        'friend_list':friend_list,
        'friend_requests':friend_requests,
    })