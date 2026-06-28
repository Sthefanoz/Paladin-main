from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_not_required
from django.urls import path

from . import views

urlpatterns = [
    path(
        'login/',
        login_not_required(
            auth_views.LoginView.as_view(template_name='registration/login.html')
        ),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
]
