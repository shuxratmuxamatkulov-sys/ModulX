from django.contrib import admin
from .models import Yarn, Fabric

@admin.register(Yarn)
class YarnAdmin(admin.ModelAdmin):
    list_display = ('name', 'title_num', 'quantity_kg', 'supplier')
    search_fields = ('name', 'supplier')

@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'density', 'quantity_kg', 'quantity_rolls')
    search_fields = ('name', 'color')