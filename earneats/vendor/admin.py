from django.contrib import admin
from vendor.models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['user', 'vendor_name', 'is_approved', 'created_at']
    list_display_links = ['user', 'vendor_name']
    prepopulated_fields = {'vendor_slug': ('vendor_name', 'user',)}
    list_filter = ['is_approved', 'created_at']
    search_fields = ['user__email', 'vendor_name']
    ordering = ['-created_at']


