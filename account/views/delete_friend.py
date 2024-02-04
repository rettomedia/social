from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from account.models import FriendRequest
from django.db.models import Q
from core.models import CustomUser

@login_required
def delete_friend(request, username):
    user = get_object_or_404(CustomUser, username=username)
    friend_request = get_object_or_404(FriendRequest, Q(from_user=user) | Q(to_user=user))
    if friend_request:
        friend_request.delete()
        return redirect('profile')