from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Yarn, Fabric
from .serializers import YarnSerializer, FabricSerializer


class YarnViewSet(viewsets.ModelViewSet):
    queryset = Yarn.objects.all()
    serializer_class = YarnSerializer
    permission_classes = [AllowAny]


class FabricViewSet(viewsets.ModelViewSet):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer
    permission_classes = [AllowAny]