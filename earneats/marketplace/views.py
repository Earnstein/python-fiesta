from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from vendor.models import Vendor
from menu.models import Category, FoodItem
from .models import Cart
from .utils import is_ajax

def marketplace(request):
    vendor_list = Vendor.approved.all().order_by("vendor_name")
    paginator = Paginator(vendor_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        vendors = paginator.page(page_number)
    except EmptyPage:
        vendors = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        vendors = paginator.page(1)
    context = {"vendors":vendors}
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = (
        vendor.category.all()
        .order_by("category_name")
        .prefetch_related(
            Prefetch("fooditems", queryset=FoodItem.objects.filter(is_available=True))
        )
    )
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else None
    context = {"vendor": vendor, "categories": categories, "cart_items": cart_items}
    return render(request, "marketplace/vendor_detail.html", context)


def add_to_cart(request, food_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "failed", "message": "Please log in to proceed"})

    if not is_ajax(request):
        return JsonResponse({"status": "failed", "message": "Invalid request"})

    food_item = FoodItem.objects.filter(id=food_id).first()
    if not food_item:
        return JsonResponse({"status": "failed", "message": "Food item does not exist"})

    cart, created = Cart.objects.get_or_create(
        user=request.user,
        fooditem=food_item,
    )
    if not created:
        cart.quantity += 1
        cart.save()

    return JsonResponse({"status": "success", "message": f"{food_item.food_title} added to cart successfully"})


def remove_from_cart(request, food_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "failed", "message": "Please log in to proceed"})

    if not is_ajax(request):
        return JsonResponse({"status": "failed", "message": "Invalid request"})

    food_item = FoodItem.objects.filter(id=food_id).first()
    if not food_item:
        return JsonResponse({"status": "failed", "message": "Food item does not exist"})

    cart = Cart.objects.filter(user=request.user, fooditem=food_item).first()

    if not cart:
        return JsonResponse({"status": "success", "message": "Your cart is empty"})
    
    if cart and cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    else:
        cart.delete()

    return JsonResponse({"status": "success", "message": f"{food_item.food_title} removed from cart successfully"})