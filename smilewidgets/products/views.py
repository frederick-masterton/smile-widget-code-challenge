from rest_framework import viewsets

from .models import ProductPrice
from .serializers import ProductPriceSerializer

class ProductPriceViewSet(viewsets.ModelViewSet):
    serializer_class = ProductPriceSerializer
    queryset = ProductPrice.objects.all()