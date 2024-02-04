from django.db import models
from core.models import CustomUser


class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user', null=True, blank=True)
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user', null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'friendrequest'
        verbose_name = 'Friend Request'
        verbose_name_plural = 'Friend Requests'