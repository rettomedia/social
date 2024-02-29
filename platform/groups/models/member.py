from django.db import models
from groups.models import Group
from network.models import CustomUser


class Member(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='group')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'member'
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        return f'{self.user.username} at {self.group.title}'