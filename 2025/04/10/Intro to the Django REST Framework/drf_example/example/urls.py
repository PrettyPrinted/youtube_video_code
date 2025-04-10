from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from app import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('coupons/', views.CouponAPIView.as_view()),
] + router.urls
