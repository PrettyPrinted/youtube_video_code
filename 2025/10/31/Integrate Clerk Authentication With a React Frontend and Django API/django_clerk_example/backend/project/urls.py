from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/videos/', views.VideoListView.as_view(), name='video-list'),
]
