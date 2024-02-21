from django.urls import path
from account.views import *

urlpatterns = [
    path('', index, name='account_index'),
    path('settings/', settings, name='settings'),
    path('profile/', profile, name='profile'),
]