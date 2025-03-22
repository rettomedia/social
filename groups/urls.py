from django.urls import path
from groups.views import *

urlpatterns = [
    path('', index, name='group_index'),
    path('join-group/<slug:group_slug>/', join_group, name='join_group'),
    path('leave-group/<slug:group_slug>/', leave_group, name='leave_group')
]