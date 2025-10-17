from django.db import models
from network.models import CustomUser


class Friend(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='from_user')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='to_user')
    is_accepted = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'friend'
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'