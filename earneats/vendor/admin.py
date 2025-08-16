from django.contrib import admin
from vendor.models import Vendor, OpeningHours, DAY_OF_WEEK_CHOICES

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['user', 'vendor_name', 'is_approved', 'created_at']
    list_display_links = ['user', 'vendor_name']
    prepopulated_fields = {'vendor_slug': ('vendor_name', 'user',)}
    list_filter = ['is_approved', 'created_at']
    search_fields = ['user__email', 'vendor_name']
    ordering = ['-created_at']


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'get_day_name', 'get_formatted_hours', 'is_currently_open']
    list_filter = ['is_open', 'day_of_week']
    search_fields = ['vendor__vendor_name']
    ordering = ['day_of_week']

    def get_day_name(self, obj):
        return dict(DAY_OF_WEEK_CHOICES)[obj.day_of_week]
    get_day_name.short_description = 'Day'
    get_day_name.admin_order_field = 'day_of_week'

    def get_formatted_hours(self, obj):
        return obj.get_formatted_hours()
    get_formatted_hours.short_description = 'Hours'
    get_formatted_hours.admin_order_field = 'from_hour'

    def is_currently_open(self, obj):
        return obj.is_currently_open()
    is_currently_open.short_description = 'Currently Open'
    is_currently_open.admin_order_field = 'is_open'