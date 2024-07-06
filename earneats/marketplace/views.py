from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from vendor.models import Vendor

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
    vendor = Vendor.approved.get(vendor_slug=vendor_slug)
    categories = vendor.category.all()
    context = {"vendor":vendor, "categories":categories}
    return render(request, 'marketplace/vendor_detail.html', context)