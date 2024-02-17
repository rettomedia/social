from django.urls import path
from network.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(
        template_name='network/login.jinja'
    ), name='login'),
    path('@<str:username>/', view_profile, name='view_profile'),
]