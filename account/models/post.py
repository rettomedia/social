from django.db import models
from core.models import CustomUser
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField


class Post(models.Model):
    title = models.CharField(max_length=70)
    content = RichTextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    writed_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title