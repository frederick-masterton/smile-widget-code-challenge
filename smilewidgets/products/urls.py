from django.urls import path, include

from rest_framework import routers

from .views import ProductPriceViewSet


router = routers.DefaultRouter()
router.register(r'get-price', ProductPriceViewSet)


urlpatterns = [
    path(r'', include(router.urls)),
]