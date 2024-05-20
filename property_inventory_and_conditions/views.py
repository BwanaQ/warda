from django.shortcuts import (
    render,
    reverse,
    redirect
)
from django.forms import (
    formset_factory
)
from django.http.response import (
    HttpResponseRedirect
)
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib import messages
from property_inventory_and_conditions.models import (
    UnitConditionQuestionTemplate,
    UnitInventoryCategory,
    UnitInventoryItem,
)
from property_inventory_and_conditions.forms import(
    UnitInventoryItemFormset 
)
from portfolio.models import ( 
    Unit
)


# Create your views here.

class UnitInventoryView(generic.View):
    template_name = 'unit_inventory/add-unit-inventory.html'

    def post(self, request,pk):
        unit = Unit.objects.get(id=pk)
        unit_inventory_items = UnitInventoryItem.objects.filter(unit=unit)
        formset = UnitInventoryItemFormset(request.POST or None)

        if formset.is_valid():
            formset.instance = unit
            formset.save()
            messages.success(request, 'Unit inventory items successfully updated')
            return redirect('add-unit-inventory',pk=unit.id)
        context = {
            'formset':formset,
            'unit_inventory_items':unit_inventory_items,
            'unit': unit
        }

        return render(request,template_name=self.template_name,context=context)


    def get(self, request,pk):
        unit = Unit.objects.get(id=pk)
        unit_inventory_items = UnitInventoryItem.objects.filter(unit=unit)
        formset = UnitInventoryItemFormset(queryset=unit_inventory_items)
        context = {
            'formset':formset,
            'unit_inventory_items':unit_inventory_items,
            'unit':unit
        }
        return render(request,template_name=self.template_name,context=context)

            


    




    
