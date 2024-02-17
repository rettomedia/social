from django.db import models
from network.models import CustomUser


class News(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.ImageField(upload_to='news/', blank=True, null=True)

    class Meta:
        db_table = 'news'
        verbose_name = 'New'
        verbose_name_plural = 'News'