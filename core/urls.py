from django.urls import path
from core.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='core/login.jinja'
    ), name='login'),
    path('logout/', logout, name='logout'),

    path('@<str:username>/', view_profile, name='view_profile'),
    path('@<str:username>/<slug:post_slug>/', post_detail, name='post_detail')
]