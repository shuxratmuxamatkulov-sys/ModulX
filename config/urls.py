from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from finance.views import AccountViewSet, TransactionViewSet
from inventory.views import YarnViewSet, FabricViewSet
from production.views import (
    ProductionRecipeViewSet,
    ProductionOrderViewSet,
    OrderViewSet,
    YarnIncomeViewSet,
    YarnIssueViewSet,
    YarnReturnViewSet,
    YarnRefundToClientViewSet,
    FabricIncomeViewSet,
    FabricDispatchViewSet
)

router = DefaultRouter()

# Inventory (Ombor) yo'nalishlari
router.register(r'yarns', YarnViewSet, basename='yarn')
router.register(r'fabrics', FabricViewSet, basename='fabric')

# Production (Ishlab chiqarish va Harakatlar) yo'nalishlari
router.register(r'recipes', ProductionRecipeViewSet, basename='recipe')
router.register(r'production-orders', ProductionOrderViewSet, basename='production-order')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'yarn-incomes', YarnIncomeViewSet, basename='yarn-income')
router.register(r'yarn-issues', YarnIssueViewSet, basename='yarn-issue')
router.register(r'yarn-returns', YarnReturnViewSet, basename='yarn-return')
router.register(r'yarn-refunds', YarnRefundToClientViewSet, basename='yarn-refund')
router.register(r'fabric-incomes', FabricIncomeViewSet, basename='fabric-income')
router.register(r'fabric-dispatches', FabricDispatchViewSet, basename='fabric-dispatch')

# Finance (Moliya) yo'nalishlari
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')


# Asosiy sahifa uchun tezkor status ko'rsatkichi
def home_view(request):
    return JsonResponse({
        'status': 'online',
        'message': 'ModulX ERP API muvaffaqiyatli ishlamoqda!',
        'documentation': '/api/docs/'
    })


urlpatterns = [
    # Asosiy sahifa
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),

    # Barcha REST API yo'nalishlari
    path('api/', include(router.urls)),

    # JWT Token olish va yangilash (Telegram Bot va boshqa servislar uchun)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger va OpenAPI Schema yo'nalishlari
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]