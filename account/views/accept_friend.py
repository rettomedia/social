from django.shortcuts import redirect, get_object_or_404
from network.models import CustomUser
from account.models import Friend
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def accept_friend(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if user != request.user:
        friend_request = get_object_or_404(
            Friend,
            Q(from_user=user) |
            Q(to_user=user), is_accepted=False
        )

        friend_request.is_accepted = True
        friend_request.save()

        return redirect('friend_list')