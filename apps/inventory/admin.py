from django.contrib import admin
from .models import Inventory, InventoryLog

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display  = ['product','stock_qty','reorder_level','unit','is_low','last_updated']
    list_filter   = ['product__category']
    search_fields = ['product__name']
    ordering      = ['product__name']

@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display  = ['product','change_qty','reason','changed_by','created_at']
    list_filter   = ['product__category']
    ordering      = ['-created_at']
