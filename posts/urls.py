from django.urls import path
from posts.views import *

urlpatterns = [
    path('add-post/', add_post, name='add_post'),
    path('like-post/<slug:post_slug>/', like_post, name='like_post'),
    path('<str:username>/<slug:post_slug>/', post_detail, name='post_detail'),
    path('delete-comment/<int:comment_id>', delete_comment, name='delete_comment')
]