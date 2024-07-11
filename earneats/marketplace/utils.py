from .models import Cart

def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

def get_total_cart_quantity(user):
    cart_items = Cart.objects.filter(user=user)
    total_quantity = sum(cart_item.quantity for cart_item in cart_items)
    return total_quantity