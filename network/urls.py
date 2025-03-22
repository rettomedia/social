from django.urls import path
from network.views import *
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404


urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(
        template_name='network/login.jinja'
    ), name='login'),
    path('help-center/', help_center, name='help_center'),
    path('@<str:username>/', view_profile, name='view_profile'),
]

handler404 = custom_404_view
