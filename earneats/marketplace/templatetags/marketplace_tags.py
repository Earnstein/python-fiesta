from django import template
from vendor.models import Vendor
from ..utils import get_total_cart_quantity

register = template.Library()


@register.simple_tag(name='active_vendors')
def total_vendors():
    """Returns the total numbers of approved vendors."""
    return Vendor.approved.count()

@register.simple_tag(name='total_cart_quantity')
def total_cart_quantity(user):
    """Returns the total quantity of items in the user's cart."""
    return get_total_cart_quantity(user)
