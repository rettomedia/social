from django.db import models
from network.models import CustomUser
from posts.models import Post


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(max_length=250)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='comments')
    writed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.message