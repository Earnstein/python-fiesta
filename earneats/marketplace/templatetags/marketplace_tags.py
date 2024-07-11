from django import template
from vendor.models import Vendor
from ..models import Cart

register = template.Library()


@register.simple_tag(name='active_vendors')
def total_vendors():
    """Returns the total numbers of approved vendors."""
    return Vendor.approved.count()

@register.simple_tag(name='total_cart_quantity')
def total_cart_quantity(user):
    """Returns the total quantity of items in the user's cart."""
    cart_items = Cart.objects.filter(user=user)
    total_quantity = sum(cart_item.quantity for cart_item in cart_items)
    return total_quantity
