from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from network.models import CustomUser
from account.models import Friend

@login_required
def delete_friend(request, username):
    user = get_object_or_404(CustomUser, username=username)

    if user != request.user:
        # İlgili arkadaşlık ilişkisini bul ve sil
        Friend.objects.filter(
            Q(from_user=user, to_user=request.user) | 
            Q(from_user=request.user, to_user=user)
        ).delete()

    return redirect('friend_list')
