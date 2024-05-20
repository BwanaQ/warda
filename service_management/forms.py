from django import forms
from crispy_forms.helper import  FormHelper
from crispy_forms.layout import  Submit
from service_management.models import (
    ServiceCategory
)

class ServiceRequestForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    service_category = forms.ModelChoiceField(label='Choose Category',queryset=ServiceCategory.objects.all(), empty_label="(Nothing)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('submit', 'Submit'))



class ServiceRequestProposalForm(forms.Form):
    # subject = forms.CharField(label='Subject', max_length=100)    
    description = forms.CharField(label='Description', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('submit', 'Submit'))
