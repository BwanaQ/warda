from .models import (
    Application,
    LeaseType,
)
from authentication import models
from portfolio import models
from django import forms
from authentication.models import (
    Tenant
)
from portfolio.models import (
    Unit
)


LEASE_TYPE_CHOICES = [('M','Month to Month Lease')]


class LeaseTypeForm(forms.Form):
    """Lease type form"""
    name = forms.CharField(label='Lease Type', widget=forms.RadioSelect(choices=LEASE_TYPE_CHOICES))
    start_date = forms.DateField(label="Beginning Date",widget=forms.DateInput(attrs={'type':'date', 'id':'start_date'}))

    #TODO Add function to dynamically render field when standard lease is chosen
    # end_date =  forms.DateField(label="End Date",widget=forms.DateInput(attrs={'type':'date', 'id':'end_date','class':'d-none'}))



class UnitTypeForm(forms.Form):
    """Housing Type Form"""
    unit_type = forms.ModelChoiceField(queryset=models.UnitType.objects.all())
    no_of_bedrooms = forms.IntegerField(label='Number of Bedrooms')
    no_of_bathrooms = forms.IntegerField(label='Number of Bathrooms')

class ParkingAndStorageForm(forms.Form):
    """Parking and Storage"""
    has_parking = forms.BooleanField(label='Has Parking')
    spaces_included = forms.IntegerField(label='Spaces Included')
    storage_spaces = forms.IntegerField(label='Storage Spaces')

class FurnishingForm(forms.Form):
    """Furnishings"""
    has_furnishing = forms.BooleanField(label='Has Furnishing')
    
class ConditionOfPremiseForm(forms.Form):
    """Condition of the Premises"""
    has_condition_of_premise = forms.BooleanField(label='Has Condition Of Premise')
    condition_of_premise = forms.CharField(label='Condition Of Premise', widget=forms.Textarea)

class PremiseDetailForm(forms.Form):
    """Additional Description"""
    has_premise_details = forms.BooleanField(label='Has Premise Details')
    premise_details = forms.CharField(label='Premise Details', widget=forms.Textarea)

class LeadDisclosureForm(forms.Form):
    """Lead Disclosure"""
    has_lead_disclosure = forms.BooleanField(label='Has Lead Disclosure')
    lead_disclosure = forms.CharField(label='Lead Disclosure', widget=forms.Textarea)
    lead_based_hazards = forms.BooleanField(label='Has Lead Disclosure')
    lead_based_hazards_details = forms.CharField(label='Lead Based Hazards Details', widget=forms.Textarea)
    landlord_has_agent = forms.BooleanField(label='Has Lead Disclosure')

class PartiesForm(forms.Form):
    """Parties"""
    landlord_name = forms.CharField(label='Landlord Name')
    tenant_name = forms.CharField(label='Tenant Name')

class ApproveApplicationForm(forms.Form):
    """Lease type form"""
    tenant = forms.ModelChoiceField(queryset=Tenant.objects.all(),empty_label="(Nothing)")
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(),empty_label="(Nothing)")




# create LeaseInfo form 
# class LeaseInfoForm(forms.ModelForm):
#     class Meta:
#         model = models.LeaseInfo
#         fields = [
#             'lease_type',
#             'is_sub_leasing_allowed',
#             'application_fee',
#             'security_deposit',
#             'is_lease_termination_allowed',
#             'lease_termination_cost',
#             'lease_term',
#             'lease_term_in_months',
#             'additional_lease_clauses',
#             'monthly_rent',
#             'utilities_deposit',
#             'total_rent'
#         ]
