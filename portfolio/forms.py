# forms.py
from django import forms
from django.contrib.gis import forms as gis_forms
from .models import Building, Unit

class LeafletWidget(gis_forms.OSMWidget):
    template_name = 'gis/leaflet.html'  # Custom template for Leaflet

class BuildingCreateForm(gis_forms.ModelForm):
    location = gis_forms.PointField(
        srid=4326,
        widget=LeafletWidget(
            attrs={
                'map_width': 600,
                'map_height': 400,
                'default_lat': -1.2921,
                'default_lon': 36.8219,
                'default_zoom': 14
            }
        )
    )
    
    class Meta:
        model = Building
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BuildingUpdateForm(gis_forms.ModelForm):
    location = gis_forms.PointField(
        srid=4326,
        widget=LeafletWidget(
            attrs={
                'map_width': 600,
                'map_height': 400,
                'default_lat': -1.2921,
                'default_lon': 36.8219,
                'default_zoom': 14
            }
        )
    )
    
    class Meta:
        model = Building
        fields = ['name', 'description', 'image', 'location', 'has_parking', 'has_parking_description', 'has_elevator', 'has_garden', 'has_swimming_pool', 'has_gym', 'has_play_area', 'has_play_area_description']

class UnitCreateForm(gis_forms.Form):
    class Meta:
        model = Unit
        exclude = ['date_added','is_occupied','likes', 'building']