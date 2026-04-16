from django.contrib import admin
from django.urls import path, include
from oauth2_provider import urls as oauth2_urls, views
from oauth_dcr.views import DynamicClientRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forum.urls')),
    path('', include('user_profile.urls')),
    path('', include('mcp_server.urls')),
    path('', include(oauth2_urls)),
    path('register', DynamicClientRegistrationView.as_view(), name='oauth_dcr'),
    path('token', views.TokenView.as_view(), name="token_without_slash"),
]
