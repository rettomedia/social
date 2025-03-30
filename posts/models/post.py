from django.db import models
from autoslug import AutoSlugField
from network.models import CustomUser
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.core.cache import cache
from network.models import Regions
import re


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    slug = AutoSlugField(unique=True, populate_from='message', always_update=True)
    writed_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    region = models.ForeignKey(Regions, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'post'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def clean(self):
        cleaned_content = re.sub(r'\n{3,}', '\n\n', self.content)
        
        if self.content != cleaned_content:
            raise ValidationError("Çok fazla boş satır ekleyemezsiniz. Lütfen içeriği düzenleyin.")

        self.content = cleaned_content 

    def save(self, *args, **kwargs):
        if self.author:
            last_post = Post.objects.filter(author=self.author).order_by('-writed_at').first()
            
            if last_post:
                if (now() - last_post.writed_at) < timedelta(seconds=30):
                    raise ValidationError('You post too often, please wait a bit!')
                if last_post.message == self.message:
                    raise ValidationError("You cannot re-share the same content!")
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.message