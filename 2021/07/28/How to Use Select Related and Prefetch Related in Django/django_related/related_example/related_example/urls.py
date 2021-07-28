import debug_toolbar

from django.contrib import admin
from django.urls import path, include

from example import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('__debug__/', include(debug_toolbar.urls)),
]