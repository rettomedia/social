from django.shortcuts import render
from account.models import Friend
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def friend_list(request):
    # Kabul edilen arkadaşlar (İki yönlü kontrol)
    friend_list = Friend.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user), is_accepted=True
    )

    # Yalnızca size gelen istekleri al (Sizin gönderdiğiniz istekleri filtreleme!)
    friend_requests = Friend.objects.filter(
        to_user=request.user, is_accepted=False
    )

    # Arama fonksiyonu
    search = request.GET.get('search')
    if search:
        friend_list = friend_list.filter(
            Q(from_user__username__icontains=search) |
            Q(to_user__username__icontains=search)
        ).distinct
