from rest_framework import viewsets
from .models import ProductionRecipe, ProductionOrder
from .serializers import ProductionRecipeSerializer, ProductionOrderSerializer

class ProductionRecipeViewSet(viewsets.ModelViewSet):
    queryset = ProductionRecipe.objects.all()
    serializer_class = ProductionRecipeSerializer

class ProductionOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrder.objects.all()
    serializer_class = ProductionOrderSerializer