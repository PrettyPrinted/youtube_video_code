from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<programmer_id>/', views.index, name='index'),
]