from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import FriendRequest
from core.models import CustomUser

@login_required
def accept_request(request, username):
    from_user = get_object_or_404(CustomUser, username=username)
    to_user = request.user

    if to_user != from_user:
        friend_request = get_object_or_404(FriendRequest, from_user=from_user, to_user=to_user)
        if friend_request:
            friend_request.is_accepted = True
            friend_request.save()
            return redirect('notifications')