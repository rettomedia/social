from django.db import models
from account.models import Post
from core.models import CustomUser


class Comment(models.Model):
    comment = models.TextField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    writed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.comment