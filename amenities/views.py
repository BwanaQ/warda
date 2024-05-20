from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import Amenity
from django.db.models import Q

def map_view(request):
    # Static reference point coordinates
    ref_latitude = -1.367447
    ref_longitude = 38.013339

    # Reference point
    ref_point = Point(ref_longitude, ref_latitude, srid=4326)

    # Retrieve amenities within 5 km radius
    amenities = Amenity.objects.filter(
            Q(point_location__distance_lte=(ref_point, 5000)) |
            Q(polygon_location__distance_lte=(ref_point, 5000))
        )
    # Pass amenities to template
    context = {
        'ref_latitude': ref_latitude,
        'ref_longitude': ref_longitude,
        'amenities': amenities
    }

    return render(request, 'amenities/map.html', context)
