from rest_framework import viewsets
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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


# ==========================================
# API VIEWSETS (Мобил бот ва бошқалар учун)
# ==========================================

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


# ==========================================
# MIJOZLAR PORTALI (Web Interface)
# ==========================================

@login_required
def client_portal(request):
    """Мижозлар ўз кабинетида ўз маълумотларини кўриши учун веб-кўриниш"""
    client_name = request.user.username

    # Мижоз номига қараб маълумотларни саралаб оламиз
    orders = Order.objects.filter(client_name__icontains=client_name)
    fabric_incomes = FabricIncome.objects.filter(client_name__icontains=client_name)
    fabric_dispatches = FabricDispatch.objects.filter(client_name__icontains=client_name)

    context = {
        'client_name': client_name,
        'orders': orders,
        'fabric_incomes': fabric_incomes,
        'fabric_dispatches': fabric_dispatches,
    }
    return render(request, 'production/client_portal.html', context)