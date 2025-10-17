from django.shortcuts import render, redirect
from network.models import CustomUser
from posts.models import Post, Like
from account.models import Friend
from django.db.models import Q

def view_profile(request, username):
    # Kullanıcının siteye kayıtlı olup olmadığını kontrol et
    try:
        user = CustomUser.objects.get(username=username)  # Bu satırda hata alırsanız, kullanıcı yok demektir.
    except CustomUser.DoesNotExist:
        return redirect('index')  # Eğer kullanıcı yoksa, anasayfaya yönlendir.

    # Kullanıcıya ait gönderileri al
    posts = Post.objects.filter(author=user).order_by('-id')

    if request.user.is_authenticated:
        # Kullanıcı kendi profilini görüntülemeye çalışıyorsa
        if user != request.user:
            # Arkadaşlık isteği durumu kontrolü
            friend_request_sent = Friend.objects.filter(from_user=request.user, to_user=user, is_accepted=False).exists()

            # Arkadaşlık durumu kontrolü
            is_friend = Friend.objects.filter(
                (Q(from_user=request.user, to_user=user) | Q(from_user=user, to_user=request.user)),
                is_accepted=True
            ).exists()

            # Kullanıcı beğenilerini kontrol et
            user_liked_posts = set(Like.objects.filter(from_user=request.user).values_list('post_id', flat=True))

            # Profil sayfasını render et
            return render(request, 'network/user-profile.jinja', context={
                'user': user,
                'posts': posts,
                'friend_request_sent': friend_request_sent,
                'is_friend': is_friend,
                'user_liked_posts':user_liked_posts
            })
        else:
            # Eğer kullanıcı kendi profilini görüntülüyorsa, profil sayfasına yönlendir
            return redirect('profile')
    else:
        # Giriş yapmamış kullanıcıyı anasayfaya yönlendir
        return redirect('index')
