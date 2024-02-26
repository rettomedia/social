from django.shortcuts import redirect, get_object_or_404
from account.models import Friend
from django.contrib.auth.decorators import login_required
from network.models import CustomUser
from django.db.models import Q


@login_required
def delete_friend(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if user != request.user:
        friend_request = get_object_or_404(
            Friend,
            Q(from_user=user) |
            Q(to_user=user)
        )

        friend_request.delete()

        return redirect('friend_list')