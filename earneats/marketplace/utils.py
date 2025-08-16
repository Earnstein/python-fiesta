from .models import Cart, Tax
from decimal import Decimal

def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

def get_total_cart_quantity(user):
    cart_items = Cart.objects.filter(user=user)
    total_quantity = sum(cart_item.quantity for cart_item in cart_items)
    return total_quantity



def get_total_cart_price(user):
    cart_items = Cart.objects.filter(user=user)
    user_country = user.userprofile.country

    # Calculate subtotal
    subtotal = sum(
        Decimal(item.fooditem.price) * item.quantity 
        for item in cart_items
    )

    # Get tax percentage or default to 10%
    default_tax_percentage = Decimal("10.0")
    tax_percentage = default_tax_percentage

    tax_obj = Tax.objects.filter(
        country=user_country, category="food", is_active=True
    ).first()

    if tax_obj:
        tax_percentage = Decimal(tax_obj.tax_percentage)

    # Calculate tax
    tax = (subtotal * tax_percentage / 100).quantize(Decimal("0.01"))

    # Calculate total
    total = (subtotal + tax).quantize(Decimal("0.01"))

    return {
        "subtotal": str(subtotal.quantize(Decimal("0.01"))),
        "tax": str(tax),
        "total": str(total),
    }
