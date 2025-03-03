from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
# Register your models here.
from .models import Building


class BuildingAdmin(LeafletGeoAdmin):
    settings_overrides = {
        'DEFAULT_CENTER': (-1.367447, 38.013339),  # Coordinates for Kitui
        'DEFAULT_ZOOM': 16,
    }
admin.site.register(Building, BuildingAdmin)
