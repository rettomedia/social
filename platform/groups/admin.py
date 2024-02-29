from django.contrib import admin
from groups.models import *

# Register your models here.
admin.site.register(Group)
admin.site.register(Member)