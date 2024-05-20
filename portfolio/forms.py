# from django.forms import ModelForm, HiddenInput
from .models import Building, Unit
from django.contrib.gis import forms

class BuildingCreateForm(forms.Form):
    location = forms.PointField(
        srid = 4326,
        widget = forms.OSMWidget(

            attrs = {
                'map_width': 600,
                'map_height': 400,
                'template_name': 'gis/openlayers-osm.html',
                'default_zoom':8,
                'default_lat': -1.2921,
                'default_lon': 36.8219,
                'default_zoom': 7
            }
        )

    )
            
    class Meta:
        model = Building
        exclude =  ['owner','date_added']

class UnitCreateForm(forms.Form):
    class Meta:
        model = Unit
        exclude = ['date_added','is_occupied','likes', 'building']