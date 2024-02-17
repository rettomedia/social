from django.urls import path
from posts.views import *

urlpatterns = [
    path('add-post/', add_post, name='add_post'),
]