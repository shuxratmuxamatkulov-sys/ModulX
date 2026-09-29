from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet, YarnIncomeViewSet, YarnIssueViewSet, YarnReturnViewSet,
    YarnRefundToClientViewSet, FabricIncomeViewSet, FabricDispatchViewSet,
    ProductionRecipeViewSet, ProductionOrderViewSet
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'yarn-income', YarnIncomeViewSet)
router.register(r'yarn-issue', YarnIssueViewSet)
router.register(r'yarn-return', YarnReturnViewSet)
router.register(r'yarn-refund', YarnRefundToClientViewSet)
router.register(r'fabric-income', FabricIncomeViewSet)
router.register(r'fabric-dispatch', FabricDispatchViewSet)
router.register(r'recipes', ProductionRecipeViewSet)
router.register(r'production-orders', ProductionOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]