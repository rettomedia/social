from django.urls import path
from account.views import *

urlpatterns = [
    path('', profile, name='profile'),
    path('delete/<slug:post_slug>/', delete_post, name='delete_post'),
    path('edit/<slug:post_slug>/', edit_post, name='edit_post'),
    path('settings/', settings, name='settings'),
    path('delete-comment/<int:id>/', delete_comment, name='delete_comment'),
    path('write/', write, name='write'),
    path('add-friend/<str:username>/', add_friend, name='add_friend'),
    path('notifications/', notifications, name='notifications'),
    path('accept/<str:username>/', accept_request, name='accept_request'),
    path('reject/<str:username>/', reject_request, name='reject_request'),
    path('delete-friend/<str:username>/', delete_friend, name='delete_friend'),
]