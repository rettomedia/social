from django.urls import path
from scripts.views import *

urlpatterns = [
    path('', index, name='scripts'),
    path('create', create_script, name='create_script'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('<str:username>/<slug:slug>/', script_detail, name='script_detail'),
]