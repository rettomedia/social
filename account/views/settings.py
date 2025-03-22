from django.shortcuts import render
from account.models import Friend
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def settings(request):
    # Sadece sana gelen istekleri alıyoruz
    notifications = Friend.objects.filter(
        to_user=request.user, is_accepted=False
    )

    return render(request, 'account/settings.jinja', context={
        'notifications': notifications,
    })
