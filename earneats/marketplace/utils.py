from .models import Cart
from decimal import Decimal

def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

def get_total_cart_quantity(user):
    cart_items = Cart.objects.filter(user=user)
    total_quantity = sum(cart_item.quantity for cart_item in cart_items)
    return total_quantity

def get_total_cart_price(user):
    cart_items = Cart.objects.filter(user=user)
    subtotal = sum(Decimal(item.fooditem.price) * item.quantity for item in cart_items)
    tax = '{:.2f}'.format(subtotal * Decimal(0.1))
    total = '{:.2f}'.format(subtotal + Decimal(tax))
    return {"subtotal": '{:.2f}'.format(subtotal), "tax": tax, "total": total}
