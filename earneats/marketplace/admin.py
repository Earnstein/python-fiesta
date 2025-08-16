from django.contrib import admin
from .models import Cart, Tax

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'fooditem', 'quantity', 'updated_at']
    list_filter = ['user']
    search_fields = ['user__username', 'fooditem__food_title']
    ordering = ['fooditem']

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['country', 'tax_type', 'tax_percentage', 'is_active']
    