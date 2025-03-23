from django.urls import path
from tickets.views import *

urlpatterns = [
    path('create', create_ticket, name='create_ticket'),
    path('my-tickets', my_tickets, name='my_tickets'),
    path('delete-ticket/<slug:slug>', delete_ticket, name='delete_ticket'),
]