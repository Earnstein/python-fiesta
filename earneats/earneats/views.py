from django.shortcuts import render
from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

def _extract_location_data(request):
    """Extract the search parameters from the request."""
    latitude = request.GET.get("lat")
    longitude = request.GET.get("lng")
    return {
        "latitude": latitude,
        "longitude": longitude, 
    }

def home(request):
    lat, lng = _extract_location_data(request).values()
    if lat and lng: 
        pnt = GEOSGeometry(f"POINT({lat} {lng})", srid=4326)
        vendors = Vendor.approved.filter(user_profile__location__distance_lte=(pnt, D(km=10)))
        vendors = vendors.annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")
        for vendor in vendors:
            vendor.km = round(vendor.distance.km, 1)
    else:
        vendors = Vendor.approved.all()[:8]

    context = {"vendors":vendors}
    return render(request, 'home.html', context)