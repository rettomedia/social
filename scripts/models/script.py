from django.db import models
from network.models import CustomUser
from autoslug import AutoSlugField
from .category import ScriptCategory


class Script(models.Model):
    title = models.CharField(max_length=70)
    category = models.ForeignKey(ScriptCategory, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    slug = AutoSlugField(populate_from='title', always_update=True, unique=True)
    subject = models.TextField(max_length=250)
    writed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'scripts'
        verbose_name = 'Script'
        verbose_name_plural = 'Scripts'

    def __str__(self):
        return self.title