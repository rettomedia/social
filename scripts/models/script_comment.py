from django.db import models
from network.models import CustomUser
from scripts.models import Script


class ScriptComment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='author')
    script = models.ForeignKey(Script, on_delete=models.CASCADE, null=True, blank=True, verbose_name='script')
    content = models.TextField(max_length=250, verbose_name='content')
    writed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'script_comment'
        verbose_name = 'Script Comment'
        verbose_name_plural = 'Script Comments'