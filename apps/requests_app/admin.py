from django.contrib import admin
from .models import SupplyRequest

@admin.register(SupplyRequest)
class SupplyRequestAdmin(admin.ModelAdmin):
    list_display  = ['agent','product_name','quantity','status','created_at']
    list_filter   = ['status']
    search_fields = ['product_name','agent__user__username']
    ordering      = ['-created_at']
