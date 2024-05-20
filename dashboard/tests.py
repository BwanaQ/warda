from datetime import datetime
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    ListView,
    View

)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import  Sum
from application_and_lease_management.models import LeaseType 
from formtools.wizard.views import SessionWizardView
from service_management.models import (
    ServiceCategory,
    ServiceRequest
)
from invoices.models import (
    Invoice
)
from portfolio.models import (
    Amenity, Community,
)
from application_and_lease_management.forms import (
    LeaseTypeForm,
    UnitTypeForm

)
from locations.forms import (
    AddressForm

)


FORMS = [
    ("leasetype",LeaseTypeForm),
    ("address",AddressForm),
    ("housetype",UnitTypeForm),
]


TEMPLATES = {
    "leasetype": "lease_templates/leasetype.html",
    "address": "lease_templates/address-form.html",
    "housetype": "lease_templates/housetype-form.html"
}


# Create home view here
def home_view(request):
    """Dashboard view"""
    paid_invoices_this_month = Invoice.objects.filter(date_paid__month=datetime.now().month)
    paid_invoices_this_year = Invoice.objects.filter(date_paid__year=datetime.now().year)
    # calculate total amount paid this month using aggregate
    month_revenue = paid_invoices_this_month.aggregate(Sum('amount'))['amount__sum'] or 0

    # calculate total amount paid this year using aggregate
    annual_revenue = paid_invoices_this_year.aggregate(Sum('amount'))['amount__sum'] or 0


    context = {
        'monthly_revenue': month_revenue,
        'annual_revenue': annual_revenue,
    }

    return render(request, 'dashboard.html',context)

class AmenityCreateView(SuccessMessageMixin,CreateView):
    """Create view for Amenity"""
    model = Amenity
    fields = ['name','description']
    template_name = 'amenities/amenity_create.html'
    success_message = 'Amenity successfully created!'
    error_message = 'Error saving the Amenity, check fields below.'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('amenity-list')

class AmenityUpdateView(SuccessMessageMixin,UpdateView):
    """Update view for Amenity"""
    model = Amenity
    fields = ['name','description']
    template_name = 'amenities/edit_amenity.html'
    success_message = 'Amenity successfully updated!'
    error_message = 'Error saving the Amenity, check fields below.'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('amenity-list')



"""Amenity Views"""
class AmenityDeleteView(SuccessMessageMixin,DeleteView):
    """Delete view for Amenity"""
    model = Amenity
    template_name = 'confirm_delete.html'
    success_message = 'Amenity successfully deleted!'
    error_message = 'Error deleteing Amenity.'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(AmenityDeleteView, self).post(request, *args, **kwargs)

    def get_object(self):
        id_ = self.kwargs.get('id')
        if not id_:
            messages.error(self.request, self.error_message)
        return get_object_or_404(Amenity, id=id_)

    def get_success_url(self):
        return reverse('amenity-list')


class AmenityDetailView(DetailView):
    """Detail view for Amenity"""
    model = Amenity
    template_name = 'amenities/amenity_detail.html'
    context_object_name = 'amenity'

    

class  AmenityListView(ListView):
    """List view for Amenity"""
    model = Amenity
    context_object_name = 'amenity_list'   # your own name for the list as a template variable
    template_name = 'amenities/amenity_list.html'

    def get_queryset(self):
        """Return all Amenity objects"""
        return Amenity.objects.all()


"""Community Views"""
class CommunityCreateView(SuccessMessageMixin,CreateView):
    """Create view for Community"""
    model = Community
    fields = ['name','address']
    template_name = 'communities/community_create.html'
    success_message = 'Community successfully created!'
    error_message = 'Error saving the Community, check fields below.'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('community-list')

class CommunityUpdateView(SuccessMessageMixin,UpdateView):
    """Update view for Community"""
    model = Community
    fields = ['name','address']
    template_name = 'communities/edit_community.html'
    success_message = 'Community successfully updated!'
    error_message = 'Error saving the Community, check fields below.'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('community-list')

class CommunityDeleteView(SuccessMessageMixin,DeleteView):
    """Delete view for Community"""
    model = Community
    template_name = 'confirm_delete.html'
    success_message = 'Community successfully deleted!'
    error_message = 'Error deleteing Community.'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(CommunityDeleteView, self).post(request, *args, **kwargs)

    def get_object(self):
        id_ = self.kwargs.get('id')
        if not id_:
            messages.error(self.request, self.error_message)
        return get_object_or_404(Community, id=id_)

    def get_success_url(self):
        return reverse('community-list')


class CommunityDetailView(DetailView):
    """Detail view for Community"""
    model = Community
    template_name = 'communities/community_detail.html'
    context_object_name = 'community'

    

class  CommunityListView(ListView):
    """List view for Community"""
    model = Community
    context_object_name = 'community_list'   # your own name for the list as a template variable
    template_name = 'communities/community_list.html'

    def get_queryset(self):
        """Return all Community objects"""
        return Community.objects.all()

class OnboardingView(View):
    template_name = 'onboarding/landlord.html'

    def get(self, request, *args, **kwargs):
        return render(request,template_name=self.template_name,context={})

class AddLeaseTemplateView(SessionWizardView):

    template_name = 'lease_templates/wizard.html'
    

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    


    def done(self, form_list, **kwargs):
        form_data =  [form.cleaned_data for form in form_list]

        d= print(form_data[0])
        # LeaseType.objects.create(**form_data[0])
        # {'lease_type': 'S', 'start_date': datetime.date(2000, 1, 1), 'end_date': datetime.date(2000, 1, 1)}
        return render(self.request, 'done.html', {
            'data': form_data,
        })


class ServiceCategoryCreateView(SuccessMessageMixin,CreateView):
    """Create view for Amenity"""
    model = ServiceCategory
    fields = ['name','description']
    template_name = 'service_categories/create_service_category.html'
    success_message = 'Service category successfully created!'
    error_message = 'Error saving the service category, check fields below.'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('service-categories')