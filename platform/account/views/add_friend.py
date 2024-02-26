from django.shortcuts import get_object_or_404, HttpResponseRedirect
from network.models import CustomUser
from django.contrib.auth.decorators import login_required
from account.models import Friend
from django.urls import reverse


@login_required
def add_friend(request, username):
    to_user = get_object_or_404(CustomUser, username=username)
    if to_user != request.user:
        Friend.objects.create(from_user=request.user, to_user=to_user)
        return HttpResponseRedirect(reverse('view_profile', args=[to_user.username]))