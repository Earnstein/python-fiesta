from vendor.models import Vendor


def get_vendor(request):
    vendor = None
    if request.user.is_authenticated:
        try:
            vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            pass
    return dict(vendor=vendor)