from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('myprofile/<str:username>', views.profile, name='profile'),
]
