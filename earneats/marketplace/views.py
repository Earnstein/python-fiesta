from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch

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
    categories = vendor.category.all().order_by("category_name").prefetch_related(
        Prefetch("fooditems", queryset=FoodItem.objects.filter(is_available=True))
    )
    context = {"vendor":vendor, "categories":categories}     
    return render(request, 'marketplace/vendor_detail.html', context)