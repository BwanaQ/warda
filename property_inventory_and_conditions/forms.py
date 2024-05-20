from django import forms
from django.forms.models import (
    formset_factory,
    modelformset_factory,
    inlineformset_factory,
    modelform_factory
)
from .models import (
    UnitInventoryCategory,
    UnitInventoryItem
)

from portfolio.models import (
    Unit
)


class UnitInventoryItemForm(forms.ModelForm):
    class Meta:
        model = UnitInventoryItem
        fields = ['name','quantity','description','category']
        label = {
            'name': 'Unit Category',
            'quantity': 'Quantity',
            'description': 'Description',
        }


UnitInventoryItemFormset = inlineformset_factory(
    Unit,
    UnitInventoryItem,
    form= UnitInventoryItemForm,
    min_num=1, # minimum number of forms
    extra=0,# number of empty forms to display
    can_delete=False # whether the forms can be deleted
)
