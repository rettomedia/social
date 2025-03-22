from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    background_image = models.ImageField(upload_to='background_images/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_blocked = models.BooleanField(default=False)


    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username