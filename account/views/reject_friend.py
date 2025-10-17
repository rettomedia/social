from django.shortcuts import redirect, get_object_or_404
from network.models import CustomUser
from account.models import Friend
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def reject_friend(request, username):
    user = get_object_or_404(CustomUser, username=username)
    
    if user != request.user:
        friend_requests = Friend.objects.filter(
            Q(from_user=user, to_user=request.user) |
            Q(from_user=request.user, to_user=user),
            is_accepted=False
        )

        friend_requests.delete()  # Birden fazla kayıt varsa hepsini siler

    return redirect('friend_list')
