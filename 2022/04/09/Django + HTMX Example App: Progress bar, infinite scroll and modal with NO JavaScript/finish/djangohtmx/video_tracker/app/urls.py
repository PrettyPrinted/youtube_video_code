from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('channelsearch/', views.channel_search, name='channel-search'),
    path('addchannel/<channel_id>/', views.add_channel, name='add-channel'),
    path('generate/', views.generate, name='generate'),
    path('get_progress/<task_id>/', views.get_progress, name='get-progress'),
    path('get_next_rows/', views.get_next_rows, name='get-next-rows'),
    path('delete_channel/<channel_id>/', views.deletechannel, name='delete-channel'),
]
