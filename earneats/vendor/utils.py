from django.shortcuts import get_object_or_404
from .models import Vendor


def get_vendor(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    return vendor
