from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
# Register your models here.
from .models import Amenity



class AmenityAdmin(LeafletGeoAdmin):
    settings_overrides = {
        'DEFAULT_CENTER': (-1.367447, 38.013339),  # Coordinates for Kitui
        'DEFAULT_ZOOM': 16,
    }

    list_display = ('name', 'amenity_type', 'geom_type')  # Add 'geom_type' to the list display
    search_fields = ('name', 'amenity_type', 'geom_type')  # Enable searching for 'name', 'amenity_type', and 'geom_type'

admin.site.register(Amenity, AmenityAdmin)
