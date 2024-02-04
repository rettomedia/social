from django.contrib import admin
from account.models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(FriendRequest)