from django.urls import path
from account.views import *

urlpatterns = [
    path('', index, name='account_index'),
    path('settings/', settings, name='settings'),
    path('profile/', profile, name='profile'),
    path('delete-post/<slug:post_slug>/', delete_post, name='delete_post'),
    path('edit-post/<slug:post_slug>/', edit_post, name='edit_post'),
    path('add-friend/<str:username>/', add_friend, name='add_friend'),
    path('friend-list/', friend_list, name='friend_list'),
    path('delete-friend/<str:username>/', delete_friend, name='delete_friend'),
    path('accept-friend/<str:username>/', accept_friend, name='accept_friend'),
    path('reject-friend/<str:username>/', reject_friend, name='reject_name'),
]