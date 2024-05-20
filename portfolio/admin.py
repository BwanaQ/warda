from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import (
    Amenity,
    BuildingFeature,
    Building,
    Neighbour,
    NeighbourType,
    Unit,
    Community,
    UnitFeature,
    UnitType
)


admin.site.register(Community)
admin.site.register(Amenity)
admin.site.register(NeighbourType)
admin.site.register(Neighbour)
admin.site.register(BuildingFeature)
admin.site.register(UnitFeature)
admin.site.register(UnitType)
admin.site.register(Unit)

class BuildingAdmin(LeafletGeoAdmin):
    settings_overrides = {
        'DEFAULT_CENTER': (-1.367447, 38.013339),  # Coordinates for Kitui
        'DEFAULT_ZOOM': 16,
    }
    list_display = ('name', 'location')
admin.site.register(Building, BuildingAdmin)
