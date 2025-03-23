from django.db import models
from network.models import CustomUser
from autoslug import AutoSlugField

# Create your models here.
class Ticket(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='author')
    title = models.CharField(max_length=70)
    content = models.TextField(max_length=500)
    slug = AutoSlugField(unique=True, populate_from='title', always_update=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ticket'
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'