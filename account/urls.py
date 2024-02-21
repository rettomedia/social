from django.urls import path
from account.views import *

urlpatterns = [
    path('', index, name='account_index'),
    path('settings/', settings, name='settings'),
    path('profile/', profile, name='profile'),
    path('delete-post/<slug:post_slug>/', delete_post, name='delete_post'),
    path('edit-post/<slug:post_slug>/', edit_post, name='edit_post'),
]