from typing import Optional, Tuple
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from vendor.models import Vendor
import logging

logger = logging.getLogger('earneats')

def get_location_from_request(request) -> Optional[Tuple[float, float]]:
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
