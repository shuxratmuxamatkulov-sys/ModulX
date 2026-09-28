from rest_framework import serializers
from .models import ProductionRecipe, ProductionOrder

class ProductionRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionRecipe
        fields = '__all__'

class ProductionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrder
        fields = '__all__'