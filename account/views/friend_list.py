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

    # Arama fonksiyonu (friend_list içinde arama yapıyoruz)
    search = request.GET.get('search')
    if search:
        friend_list = friend_list.filter(
            Q(from_user__username__icontains=search) |
            Q(to_user__username__icontains=search)
        ).distinct()

    # **Hata önleme:** Eğer `friend_list` ve `friend_requests` boşsa bile `return` olmalı!
    return render(request, 'account/friend-list.jinja', {
        'friend_list': friend_list if friend_list.exists() else [],
        'friend_requests': friend_requests if friend_requests.exists() else []
    })
