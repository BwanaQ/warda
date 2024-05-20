from django import forms
from locations.models import *



class AddressForm(forms.ModelForm):
    """Address forms"""
    class Meta:
        Modelforms = Address
        labels = {
            'street_address': 'Street Address',
            'city': 'City',
            'state': 'State',
            'zip_code': 'Zip Code',
        }
        fields = ['street_address','city','state','zip_code']