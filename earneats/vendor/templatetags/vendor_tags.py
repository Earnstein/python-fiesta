from django import template
from django.utils import timezone
from vendor.models import OpeningHours

register = template.Library()

@register.inclusion_tag('includes/opening_hours.html', takes_context=True)
def vendor_opening_hours(context, vendor=None):
    """Display opening hours for a vendor."""
    if not vendor:
        vendor = context.get('vendor')
    
    if vendor:
        opening_hours = vendor.get_all_opening_hours()
        current_day = timezone.now().isoweekday()
        return {
            'opening_hours': opening_hours,
            'current_day': current_day
        }
    
    return {
        'opening_hours': [],
        'current_day': timezone.now().isoweekday()
    }

@register.simple_tag
def get_vendor_opening_hours(vendor):
    """Get opening hours for a vendor."""
    if vendor:
        return vendor.get_all_opening_hours()
    return []

@register.simple_tag
def get_current_day():
    """Get current day of week (Monday=1, Sunday=7)."""
    return timezone.now().isoweekday()

@register.filter
def is_current_day(opening_hours, day_of_week):
    """Check if opening hours are for current day."""
    current_day = timezone.now().isoweekday()
    return opening_hours.day_of_week == current_day

@register.filter
def get_today_hours(opening_hours_list):
    """Get today's opening hours from a list."""
    current_day = timezone.now().isoweekday()
    for hours in opening_hours_list:
        if hours.day_of_week == current_day:
            return hours
    return None

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key."""
    return dictionary.get(key)
