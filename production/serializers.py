from rest_framework import serializers
from .models import (
    ProductionRecipe, ProductionOrder, Order,
    YarnIncome, YarnIssue, YarnReturn,
    YarnRefundToClient, FabricIncome, FabricDispatch
)

class ProductionRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionRecipe
        fields = '__all__'

class ProductionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrder
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class YarnIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = YarnIncome
        fields = '__all__'

class YarnIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = YarnIssue
        fields = '__all__'

class YarnReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = YarnReturn
        fields = '__all__'

class YarnRefundToClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = YarnRefundToClient
        fields = '__all__'

class FabricIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FabricIncome
        fields = '__all__'

class FabricDispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = FabricDispatch
        fields = '__all__'