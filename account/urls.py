from django.urls import path
from account.views import *

urlpatterns = [
    path('settings/', settings, name='settings'),
    path('profile/', profile, name='profile'),
]