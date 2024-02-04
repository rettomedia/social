from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import CustomUser
from account.models import FriendRequest
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def add_friend(request, username):
    from_user = request.user
    to_user = get_object_or_404(CustomUser, username=username)

    if to_user != from_user:
        FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return HttpResponseRedirect(reverse('view_profile', args=[username]))