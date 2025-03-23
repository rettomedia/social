from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from network.models import CustomUser, News, Ticket

# Register your models here.
@admin.register(CustomUser)
class CustomAdmin(UserAdmin):
    list_display = ('username','email')
    fieldsets = UserAdmin.fieldsets + (
        ('Avatar Area', {
            'fields':['avatar']
        }),
        ('Bio Area', {
            'fields':['bio']
        })
    )

admin.site.register(News)
admin.site.register(Ticket)