from rest_framework import viewsets
from .models import (
    ProductionRecipe, ProductionOrder, Order,
    YarnIncome, YarnIssue, YarnReturn,
    YarnRefundToClient, FabricIncome, FabricDispatch
)
from .serializers import (
    ProductionRecipeSerializer, ProductionOrderSerializer, OrderSerializer,
    YarnIncomeSerializer, YarnIssueSerializer, YarnReturnSerializer,
    YarnRefundToClientSerializer, FabricIncomeSerializer, FabricDispatchSerializer
)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer

class YarnIncomeViewSet(viewsets.ModelViewSet):
    queryset = YarnIncome.objects.all().order_by('-id')
    serializer_class = YarnIncomeSerializer

class YarnIssueViewSet(viewsets.ModelViewSet):
    queryset = YarnIssue.objects.all().order_by('-id')
    serializer_class = YarnIssueSerializer

class YarnReturnViewSet(viewsets.ModelViewSet):
    queryset = YarnReturn.objects.all().order_by('-id')
    serializer_class = YarnReturnSerializer

class YarnRefundToClientViewSet(viewsets.ModelViewSet):
    queryset = YarnRefundToClient.objects.all().order_by('-id')
    serializer_class = YarnRefundToClientSerializer

class FabricIncomeViewSet(viewsets.ModelViewSet):
    queryset = FabricIncome.objects.all().order_by('-id')
    serializer_class = FabricIncomeSerializer

class FabricDispatchViewSet(viewsets.ModelViewSet):
    queryset = FabricDispatch.objects.all().order_by('-id')
    serializer_class = FabricDispatchSerializer

class ProductionRecipeViewSet(viewsets.ModelViewSet):
    queryset = ProductionRecipe.objects.all()
    serializer_class = ProductionRecipeSerializer

class ProductionOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrder.objects.all().order_by('-id')
    serializer_class = ProductionOrderSerializer