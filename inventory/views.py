from rest_framework import viewsets
from .models import Yarn, Fabric
from .serializers import YarnSerializer, FabricSerializer

class YarnViewSet(viewsets.ModelViewSet):
    queryset = Yarn.objects.all()
    serializer_class = YarnSerializer

class FabricViewSet(viewsets.ModelViewSet):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer