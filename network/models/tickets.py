from django.db import models
from network.models.user import CustomUser


class Ticket(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(max_length=500, verbose_name='ticket')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket'
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'