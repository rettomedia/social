from django.urls import path
from groups.views import *

urlpatterns = [
    path('', index, name='group_index'),
    path('join-group/<slug:group_slug>/', join_group, name='join_group'),
    path('leave-group/<slug:group_slug>/', leave_group, name='leave_group'),
    path('group-settings/<slug:group_slug>/', group_settings, name='group_settings'),
    path('group/<slug:group_slug>/', group, name='group_detail'),
]