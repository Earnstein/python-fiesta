from django.shortcuts import render
from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.utils import timezone
from typing import Optional, Tuple
import logging
import json
from django.forms.models import model_to_dict

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
        .with_opening_status_and_distance(point)
        .filter(user_profile__location__distance_lte=(point, D(km=radius_km)))
        .order_by("distance")
    )
    
    return list(vendors)

def home(request):
    """Home page view showing nearby vendors first, then other vendors to fill remaining slots."""
    MAX_VENDORS = 8
    location = _get_location_from_request(request)
    
    if location:
        lat, lng = location
        # Get nearby vendors
        nearby_vendors = _get_nearby_vendors(lat, lng)
        
        # If we have enough nearby vendors, use them
        if len(nearby_vendors) >= MAX_VENDORS:
            vendors = nearby_vendors[:MAX_VENDORS]
        else:
            # Get other vendors to fill remaining slots
            nearby_vendor_ids = [vendor.id for vendor in nearby_vendors]
            other_vendors = (
                Vendor.approved
                .with_opening_status()
                .exclude(id__in=nearby_vendor_ids)
                .order_by('?')  # Random order for variety
                [:MAX_VENDORS - len(nearby_vendors)]
            )
            
            # Combine nearby first, then others
            vendors = list(nearby_vendors) + list(other_vendors)
    else:
        # Fallback to featured vendors if no location data is available
        vendors = (
            Vendor.approved
            .with_opening_status()
            [:MAX_VENDORS]
        )

    # Check if each vendor is currently open
    context = {"vendors": vendors}
    return render(request, 'home.html', context)