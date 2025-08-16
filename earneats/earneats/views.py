from django.shortcuts import render
from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.db.models import Case, When, Value, IntegerField
from earneats.utils import get_location_from_request

def home(request):
    """
    Home page view showing nearby vendors first, then other vendors.
    """
    MAX_VENDORS = 8
    RADIUS_KM = 10
    
    location = get_location_from_request(request)
    
    # Build base queryset
    base_queryset = (
        Vendor.approved
        .with_opening_status()
        .select_related('user', 'user_profile')
        .prefetch_related('opening_hours', 'categories')
    )
    
    if location:
        lat, lng = location
        point = GEOSGeometry(f"POINT({lng} {lat})", srid=4326)
        
        # Get all vendors, prioritize nearby ones
        vendors = (
            base_queryset
            .annotate(
                distance=Distance("user_profile__location", point),
                # Create priority field: 1 for nearby, 2 for distant
                priority=Case(
                    When(
                        user_profile__location__distance_lte=(point, D(km=RADIUS_KM)), 
                        then=Value(1)
                    ),
                    default=Value(2),
                    output_field=IntegerField()
                )
            )
            .order_by('priority', 'distance', '?')  # Nearby first, then by distance, then random
            [:MAX_VENDORS]
        )
        
    else:
        # Fallback: get vendors without location consideration
        vendors = base_queryset.order_by('?')[:MAX_VENDORS]
    
    # Convert to list to avoid multiple evaluations in template
    vendors_list = list(vendors)
    
    context = {"vendors": vendors_list}
    return render(request, 'home.html', context)
