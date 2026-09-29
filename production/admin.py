from django.contrib import admin
from .models import (
    ProductionRecipe, ProductionOrder,
    Order, YarnIncome, YarnIssue, YarnReturn,
    YarnRefundToClient, FabricIncome, FabricDispatch
)

# === Существующие модели ===
@admin.register(ProductionRecipe)
class ProductionRecipeAdmin(admin.ModelAdmin):
    list_display = ('fabric', 'yarn', 'percentage')

@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'fabric', 'target_kg', 'actual_kg', 'status', 'created_at')
    list_filter = ('status',)


# === Новые добавленные модели ===
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_name', 'client_name', 'fabric_name', 'quantity_kg', 'date')
    search_fields = ('order_name', 'client_name', 'fabric_name')

@admin.register(YarnIncome)
class YarnIncomeAdmin(admin.ModelAdmin):
    list_display = ('yarn_name', 'yarn_lot', 'quantity_kg', 'supplier_company', 'income_date')
    search_fields = ('yarn_name', 'yarn_lot', 'supplier_company')

@admin.register(YarnIssue)
class YarnIssueAdmin(admin.ModelAdmin):
    list_display = ('yarn_name', 'yarn_lot', 'machine_number', 'quantity_kg', 'issue_date')
    search_fields = ('yarn_name', 'yarn_lot', 'machine_number')

@admin.register(YarnReturn)
class YarnReturnAdmin(admin.ModelAdmin):
    list_display = ('yarn_name', 'yarn_lot', 'quantity_kg', 'client_name', 'return_date')

@admin.register(YarnRefundToClient)
class YarnRefundToClientAdmin(admin.ModelAdmin):
    list_display = ('yarn_name', 'client_name', 'quantity_kg', 'refund_date')

@admin.register(FabricIncome)
class FabricIncomeAdmin(admin.ModelAdmin):
    list_display = ('fabric_name', 'client_name', 'quantity_kg', 'roll_count', 'income_date')
    search_fields = ('fabric_name', 'client_name')

@admin.register(FabricDispatch)
class FabricDispatchAdmin(admin.ModelAdmin):
    list_display = ('fabric_name', 'client_name', 'quantity_kg', 'roll_count', 'dispatch_date')
    search_fields = ('fabric_name', 'client_name')