from django import template
from vendor.models import Vendor

register = template.Library()


@register.simple_tag(name='active_vendors')
def total_vendors():
    return Vendor.approved.count()