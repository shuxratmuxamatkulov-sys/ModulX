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
from production.views import ProductionRecipeViewSet, ProductionOrderViewSet

router = DefaultRouter()

# Inventory yo'nalishlari
router.register(r'yarns', YarnViewSet, basename='yarn')
router.register(r'fabrics', FabricViewSet, basename='fabric')

# Production yo'nalishlari
router.register(r'recipes', ProductionRecipeViewSet, basename='recipe')
router.register(r'orders', ProductionOrderViewSet, basename='order')

# Finance yo'nalishlari
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')


# Asosiy sahifa uchun oddiy funksiya
def home_view(request):
  return JsonResponse({'message': 'ModulX API muvaffaqiyatli ishlamoqda!'})


urlpatterns = [
    # Asosiy sahifa
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # JWT Token olish va yangilash manzillari
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    # Swagger va OpenAPI Schema yo'nalishlari
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]