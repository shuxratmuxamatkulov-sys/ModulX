from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import ProductionRecipe, ProductionOrder
from .serializers import ProductionRecipeSerializer, ProductionOrderSerializer


class ProductionRecipeViewSet(viewsets.ModelViewSet):
    queryset = ProductionRecipe.objects.all()
    serializer_class = ProductionRecipeSerializer
    permission_classes = [AllowAny]


class ProductionOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrder.objects.all()
    serializer_class = ProductionOrderSerializer
    permission_classes = [AllowAny]