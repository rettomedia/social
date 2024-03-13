from django.urls import path
from scripts.views import *

urlpatterns = [
    path('', index, name='scripts')
]