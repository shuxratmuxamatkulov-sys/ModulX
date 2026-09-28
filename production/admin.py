from django.contrib import admin
from .models import ProductionRecipe, ProductionOrder

@admin.register(ProductionRecipe)
class ProductionRecipeAdmin(admin.ModelAdmin):
    list_display = ('fabric', 'yarn', 'percentage')

@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'fabric', 'target_kg', 'actual_kg', 'status', 'created_at')
    list_filter = ('status',)