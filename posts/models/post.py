from django.db import models
from autoslug import AutoSlugField
from network.models import CustomUser


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    slug = AutoSlugField(unique=True, populate_from='message', always_update=True)
    writed_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.message