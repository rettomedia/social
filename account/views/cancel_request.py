from django.shortcuts import redirect
from account.models import Friend

def cancel_request(request, username):
    user = request.user
    # Kullanıcının gönderdiği arkadaşlık isteğini bul
    friend_request = Friend.objects.filter(from_user=user, to_user__username=username, is_accepted=False).first()
    if friend_request:
        # İsteği sil
        friend_request.delete()
    return redirect(request.META.get('HTTP_REFERER'))  # Yönlendirilmesi gereken sayfa
