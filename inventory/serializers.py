from rest_framework import serializers
from .models import Yarn, Fabric

class YarnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yarn
        fields = '__all__'

class FabricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabric
        fields = '__all__'