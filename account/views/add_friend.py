from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from network.models import CustomUser
from account.models import Friend
from django.db.models import Q

@login_required
def add_friend(request, username):
    to_user = get_object_or_404(CustomUser, username=username)

    if to_user != request.user:
        # Önceden var olan arkadaşlık isteğini veya ilişkisini kontrol et
        existing_request = Friend.objects.filter(
            Q(from_user=request.user, to_user=to_user) | 
            Q(from_user=to_user, to_user=request.user)
        ).exists()

        if not existing_request:  # Eğer zaten yoksa, yeni istek oluştur
            Friend.objects.create(from_user=request.user, to_user=to_user, is_accepted=False)

    return HttpResponseRedirect(reverse('view_profile', args=[to_user.username]))
