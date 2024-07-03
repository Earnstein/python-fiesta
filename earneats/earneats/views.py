from django.shortcuts import render
from vendor.models import Vendor

def home(request):
    vendors = Vendor.approved.all()[:8]
    context = {"vendors":vendors}
    return render(request, 'home.html', context)