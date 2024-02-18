from django.db import models
from network.models import CustomUser
from posts.models import Post


class Like(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'like'
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return self.from_user