from django.db import models
from autoslug import AutoSlugField
from network.models import CustomUser


# Group Model
class Group(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='group_images/', blank=True, null=True)
    background = models.ImageField(upload_to='group_backgrounds/', blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    is_public = models.BooleanField(default=True)
    about = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owned_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='owned_by')

    class Meta:
        db_table = 'group'
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.title
    
    def is_member(self, user):
        return self.members.filter(user=user).exists()