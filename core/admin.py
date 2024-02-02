from django.contrib import admin
from core.models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(CustomUser)
class CustomAdmin(UserAdmin):
    list_display = ('username','email')
    fieldsets = UserAdmin.fieldsets + (
        ('Avatar Area', {
            'fields':['avatar']
        }),
        ('Bio', {
            'fields':['bio']
        })
    )