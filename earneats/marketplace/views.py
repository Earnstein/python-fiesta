from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from vendor.models import Vendor
from menu.models import FoodItem
from marketplace.models import Cart
from marketplace.utils import is_ajax, get_total_cart_quantity, get_total_cart_price


SUCCESS = "success"
FAILED = "failed"


def marketplace(request):
    vendor_list = Vendor.approved.with_opening_status().prefetch_related('opening_hours').order_by("vendor_name")
    
    paginator = Paginator(vendor_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        vendors = paginator.page(page_number)
    except EmptyPage:
        vendors = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        vendors = paginator.page(1)
    
    # Get current day for opening hours display
    current_day = timezone.now().isoweekday()
    
    context = {
        "vendors": vendors,
        "current_day": current_day
    }
    return render(request, "marketplace/listings.html", context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = (
        vendor.categories.all()
        .filter(fooditems__isnull=False)
        .distinct()
        .order_by("category_name")
        .prefetch_related(
            "fooditems",
        )
    )

    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    # Get opening hours and current day
    opening_hours = vendor.get_all_opening_hours()
    current_day = timezone.now().isoweekday()  # Monday=1, Sunday=7

    context = {
        "vendor": vendor, 
        "categories": categories, 
        "cart_items": cart_items, 
        "opening_hours": opening_hours,
        "current_day": current_day
    }
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
    cart_data = get_total_cart_price(request.user)
    return JsonResponse(
        {
            "status": SUCCESS,
            "message": f"{food_item.food_title} added to cart successfully",
            "total_quantity": total_quantity,
            "qty": cart.quantity,
            "subtotal": cart_data["subtotal"],
            "tax": cart_data["tax"],
            "total": cart_data["total"],
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
        cart_data = get_total_cart_price(request.user)
        return JsonResponse(
            {
                "status": SUCCESS,
                "message": "Your cart is empty",
                "subtotal": cart_data["subtotal"],
                "tax": cart_data["tax"],
                "total": cart_data["total"],
            }
        )

    if cart and cart.quantity > 0:
        cart.quantity -= 1
        cart.save()
    total_quantity = get_total_cart_quantity(request.user)
    cart_data = get_total_cart_price(request.user)
    return JsonResponse(
        {
            "status": SUCCESS,
            "message": f"{food_item.food_title} removed from cart successfully",
            "total_quantity": total_quantity,
            "qty": cart.quantity,
            "subtotal": cart_data["subtotal"],
            "tax": cart_data["tax"],
            "total": cart_data["total"],
        }
    )


@login_required(login_url="login")
def cart(request):
    carts = Cart.objects.filter(user=request.user).order_by("-created_at")
    page_number = request.GET.get("page", 1)
    paginator = Paginator(carts, 3)
    try:
        carts = paginator.page(page_number)
    except EmptyPage:
        carts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        carts = paginator.page(1)
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
    cart_data = get_total_cart_price(request.user)
    return JsonResponse(
        {
            "status": SUCCESS,
            "message": "Cart item deleted successfully",
            "total_quantity": total_quantity,
            "subtotal": cart_data["subtotal"],
            "tax": cart_data["tax"],
            "total": cart_data["total"],
        }
    )

def _extract_search_parameters(request):
    """Extract the search parameters from the request."""
    source_location = request.GET.get("address")
    latitude = request.GET.get("lat")
    longitude = request.GET.get("lng")
    radius = request.GET.get("radius")
    search_title = request.GET.get("search_title")
    return {
        "source_location": source_location,
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
        "search_title": search_title,
    }


def _has_location_data(search_params):
    """Check if all required location parameters are present."""
    return all([
        search_params['latitude'],
        search_params['longitude'], 
        search_params['radius']
    ])


def search(request):
    """View to search for vendors and food items."""

  
    if "address" not in request.GET:
        return redirect("marketplace")
    
    search_params = _extract_search_parameters(request)
    search_title = search_params["search_title"]

    # Get the food items that match the search title and are available
    matching_food_items = FoodItem.objects.filter(
        food_title__icontains=search_title, is_available=True
    )

    # filter the vendors by distance
    if _has_location_data(search_params):
        pnt = GEOSGeometry(f"POINT({search_params['longitude']} {search_params['latitude']})", srid=4326)
        # Get the vendors that match the search title and are approved and active 
        vendors = Vendor.approved.with_opening_status_and_distance(pnt).filter(
            Q(id__in=matching_food_items.values_list("vendor", flat=True))
            | Q(vendor_name__icontains=search_title, is_approved=True, user__is_active=True)
        ).filter(user_profile__location__distance_lte=(pnt, D(km=search_params['radius']))).order_by("distance")
    else:
        # Get the vendors that match the search title and are approved and active (no distance filtering)
        vendors = Vendor.approved.with_opening_status().filter(
            Q(id__in=matching_food_items.values_list("vendor", flat=True))
            | Q(vendor_name__icontains=search_title, is_approved=True, user__is_active=True)
        )

    context = {
        "vendors": vendors,
        "count": vendors.count(),
        "source_location": search_params["source_location"],
    }
    return render(request, "marketplace/listings.html", context)
