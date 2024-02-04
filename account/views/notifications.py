from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import FriendRequest
from core.models import CustomUser


@login_required
def notifications(request):
    friend_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False)

    return render(request, 'account/notifications.jinja', context={
        'friend_requests':friend_requests,
    })