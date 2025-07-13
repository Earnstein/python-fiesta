from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from vendor.models import Vendor
from menu.models import FoodItem
from .models import Cart
from .utils import is_ajax, get_total_cart_quantity, get_total_cart_price
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance


SUCCESS = "success"
FAILED = "failed"


def marketplace(request):
    vendor_list = Vendor.approved.all().order_by("vendor_name")
    paginator = Paginator(vendor_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        vendors = paginator.page(page_number)
    except EmptyPage:
        vendors = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        vendors = paginator.page(1)
    context = {"vendors": vendors}
    return render(request, "marketplace/listings.html", context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = (
        vendor.categories.all()
        .order_by("category_name")
        .prefetch_related(
            Prefetch("fooditems", queryset=FoodItem.objects.filter(is_available=True))
        )
    )

    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {"vendor": vendor, "categories": categories, "cart_items": cart_items}
    return render(request, "marketplace/vendor_detail.html", context)


def add_to_cart(request, food_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": FAILED, "message": "Please log in to proceed"})

    if not is_ajax(request):
        return JsonResponse({"status": FAILED, "message": "Invalid request"})

    food_item = FoodItem.objects.filter(id=food_id).first()
    if not food_item:
        return JsonResponse({"status": FAILED, "message": "Food item does not exist"})

    cart, created = Cart.objects.get_or_create(
        user=request.user,
        fooditem=food_item,
    )
    if not created:
        cart.quantity += 1
        cart.save()
    total_quantity = get_total_cart_quantity(request.user)
    subtotal, tax, total = get_total_cart_price(request.user).values()
    return JsonResponse(
        {
            "status": SUCCESS,
            "message": f"{food_item.food_title} added to cart successfully",
            "total_quantity": total_quantity,
            "qty": cart.quantity,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
        }
    )


def remove_from_cart(request, food_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": FAILED, "message": "Please log in to proceed"})

    if not is_ajax(request):
        return JsonResponse({"status": FAILED, "message": "Invalid request"})

    food_item = FoodItem.objects.filter(id=food_id).first()
    if not food_item:
        return JsonResponse({"status": FAILED, "message": "Food item does not exist"})

    cart = Cart.objects.filter(user=request.user, fooditem=food_item).first()

    if not cart or cart.quantity == 0:
        subtotal, tax, total = get_total_cart_price(request.user).values()
        return JsonResponse(
            {
                "status": SUCCESS,
                "message": "Your cart is empty",
                "subtotal": subtotal,
                "tax": tax,
                "total": total,
            }
        )

    if cart and cart.quantity > 0:
        cart.quantity -= 1
        cart.save()
    total_quantity = get_total_cart_quantity(request.user)
    subtotal, tax, total = get_total_cart_price(request.user).values()
    return JsonResponse(
        {
            "status": SUCCESS,
            "message": f"{food_item.food_title} removed from cart successfully",
            "total_quantity": total_quantity,
            "qty": cart.quantity,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
        }
    )


@login_required(login_url="login")
def cart(request):
    carts = (
        Cart.objects.filter(user=request.user).order_by("-created_at")
        if request.user.is_authenticated
        else None
    )
    context = {"carts": carts}
    return render(request, "marketplace/cart.html", context)


def delete_cart(request, cart_id):
    """View to delete a cart item."""
    if not request.user.is_authenticated:
        return JsonResponse({"status": FAILED, "message": "Please log in to proceed"})

    if not is_ajax(request):
        return JsonResponse({"status": FAILED, "message": "Invalid request"})

    cart_item = Cart.objects.filter(user=request.user, id=cart_id).first()

    if cart_item is None:
        return JsonResponse({"status": SUCCESS, "message": "Cart item does not exist"})

    cart_item.delete()
    total_quantity = get_total_cart_quantity(request.user)
    subtotal, tax, total = get_total_cart_price(request.user).values()
    return JsonResponse(
        {
            "status": SUCCESS,
            "message": "Cart item deleted successfully",
            "total_quantity": total_quantity,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
        }
    )


def search(request):
    """View to search for vendors and food items."""

  
    if "address" not in request.GET:
        return redirect("marketplace")
    
    # Get the latitude, longitude, and radius from the request
    source_location = request.GET.get("address")
    latitude = request.GET.get("lat")
    longitude = request.GET.get("lng")
    radius = request.GET.get("radius")

    # Get the search title from the request
    search_title = request.GET.get("search_title")

    # Get the food items that match the search title and are available
    food_items = FoodItem.objects.filter(
        food_title__icontains=search_title, is_available=True
    )

    # Get the vendors that match the search title and are approved and active
    vendors = Vendor.approved.filter(
        Q(id__in=food_items.values_list("vendor", flat=True))
        | Q(vendor_name__icontains=search_title, is_approved=True, user__is_active=True)
    )

    # filter the vendors by distance
    if latitude and longitude and radius:
        pnt = GEOSGeometry(f"POINT({longitude} {latitude})", srid=4326)
        vendors = (
            vendors.filter(user_profile__location__distance_lte=(pnt, D(km=radius)))
            .annotate(distance=Distance("user_profile__location", pnt))
            .order_by("distance")
        )
        for vendor in vendors:
            vendor.km = round(vendor.distance.km, 1)

    context = {
        "vendors": vendors,
        "count": vendors.count(),
        "source_location": source_location,
    }
    return render(request, "marketplace/listings.html", context)
