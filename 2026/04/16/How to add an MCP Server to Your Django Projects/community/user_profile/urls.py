from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import ExtendedAuthenticationForm

urlpatterns = [
    path('signup/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='user_profile/login.html', authentication_form=ExtendedAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
