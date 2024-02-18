from django.urls import path
from groups.views import *

urlpatterns = [
    path('', index, name='group_index')
]