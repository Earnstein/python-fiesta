from django.shortcuts import render
from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from typing import Optional, Tuple
import logging

logger = logging.getLogger('earneats')

def _get_location_from_request(request) -> Optional[Tuple[float, float]]:
    """Extract and validate location data from request session or GET params."""
    try:
        # Check session first
        if "lat" in request.session and "lng" in request.session:
            lat = float(request.session["lat"])
            lng = float(request.session["lng"])
            return lat, lng
        
        # Check GET parameters
        if "lat" in request.GET and "lng" in request.GET:
            lat = float(request.GET["lat"])
            lng = float(request.GET["lng"])
            
            # Store in session for future requests
            request.session["lat"] = lat
            request.session["lng"] = lng
            
            return lat, lng
            
    except (ValueError, TypeError) as e:
        logger.warning(f"Invalid location data: {e}")
        return None
    
    return None

def _get_nearby_vendors(lat: float, lng: float, radius_km: int = 10) -> list:
    """Get vendors within specified radius of given coordinates."""
    point = GEOSGeometry(f"POINT({lng} {lat})", srid=4326)
    
    vendors = (
        Vendor.approved
        .filter(user_profile__location__distance_lte=(point, D(km=radius_km)))
        .annotate(distance=Distance("user_profile__location", point))
        .order_by("distance")
    )
    
    # Add distance to each vendor object
    for vendor in vendors:
        vendor.km = round(vendor.distance.km, 1)
    
    return list(vendors)

def home(request):
    """Home page view showing nearby vendors or featured vendors."""
    location = _get_location_from_request(request)
    if location:
        lat, lng = location
        # Get nearby vendors or fallback to featured vendors
        vendors = _get_nearby_vendors(lat, lng) or Vendor.approved.all()[:8]
    else:
        # Fallback to featured vendors if no location data is available
        vendors = Vendor.approved.all()[:8]

    context = {"vendors": vendors}
    return render(request, 'home.html', context)