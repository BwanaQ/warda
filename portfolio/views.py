from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.contrib.gis import forms


from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,

)
from django.db.models import Sum
from .models import Building, Unit
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from invoices.models import *
from service_management.models import *
from .forms import BuildingCreateForm, BuildingUpdateForm
from django.http.response import HttpResponseRedirect

from django.urls import reverse

from django.contrib import messages


class HomeView(View):
    """Home view"""

    template_name = 'landing.html'

    def get(self, request, *args, **kwargs):
        return render(request,template_name=self.template_name,context={})

class AboutView(View):
    """About view"""

    template_name = 'about.html'

    def get(self, request, *args, **kwargs):
        return render(request,template_name=self.template_name,context={})


class PropertyListView(View):
    """Property page"""
    template_name = "property-grid.html"
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name=self.template_name, context=context)

class BuildingListView(LoginRequiredMixin, ListView):
    model = Building
    template_name = 'buildings/building_list.html'

    def get_queryset(self):
        return Building.objects.filter(owner=self.request.user)

class BuildingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'buildings/building_create.html'
    model = Building
    form_class = BuildingCreateForm
    success_url = reverse_lazy('building-list')
    success_message = "Building created successfully!"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        building = self.get_object()
        if self.request.user == building.owner:
            return True
        return False

class BuildingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Building
    form_class = BuildingUpdateForm
    template_name = 'buildings/edit_building.html'
    success_url = reverse_lazy('building-list')
    success_message = "Building successfully updated!"
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        building = self.get_object()
        if self.request.user == building.owner:
            return True
        return False

class BuildingDetailView(DetailView):
    template_name = 'buildings/building_detail.html'
    model = Building
    success_url = reverse_lazy('building_detail')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        units = Unit.objects.filter(building=self.object)
        context = self.get_context_data(object=self.object)
        context['unit_list'] = units
        context['total_units'] = units.count()


        paid_invoices_this_month = Invoice.objects.filter(building_id=self.object.id,date_paid__month=datetime.now().month)
        paid_invoices_this_year = Invoice.objects.filter(building_id=self.object.id,date_paid__year=datetime.now().year)
        unpaid_invoices_this_month = Invoice.objects.filter(building_id=self.object.id,date_paid__month=datetime.now().month, paid=False)


        # calculate total amount paid this month using aggregate
        month_revenue = paid_invoices_this_month.aggregate(Sum('amount'))['amount__sum'] or 0

        # calculate total amount paid this year using aggregate
        annual_revenue = paid_invoices_this_year.aggregate(Sum('amount'))['amount__sum'] or 0

        # calculate total amount unpaid this month using aggregate
        month_unpaid_invoices = unpaid_invoices_this_month.aggregate(Sum('amount'))['amount__sum'] or 0

        # calculate total pending service_requests requests
        pending_maintainance_requests = ServiceRequest.objects.filter(status__name='Pending').count()

        months = [1,2,3,4,5,6,7,8,9,10,11,12]
        months_name = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        # calculate total amount paid for each month from the months list above
        month_revenue_list = []

        for month in months:
            month_revenue_list.append(
                paid_invoices_this_month.filter(date_paid__month=month).aggregate(Sum('amount'))['amount__sum'] or 0
            )
        
        context['monthly_revenue'] = month_revenue 
        context.update(
        {
            'annual_revenue': annual_revenue,
            'pending_maintainance_requests': pending_maintainance_requests,
            'unpaid_invoices_this_month': month_unpaid_invoices,
            'month_revenue_list': month_revenue_list,
            'labels': months_name,
            'dataset': month_revenue_list,
            "rent_collected_this_month": [month_unpaid_invoices,month_revenue ]
    
        }

        )

        return self.render_to_response(context)



class BuildingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Building
    template_name = 'confirm_delete.html'
    success_message = "Building successfully deleted!"
    error_message = 'Error deleteing Building.'
    
    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(BuildingDeleteView, self).post(request, *args, **kwargs)

    def get_object(self):
        id_ = self.kwargs.get('id')
        if not id_:
            messages.error(self.request, self.error_message)
        return get_object_or_404(Building, id=id_)

    def get_success_url(self):
        return reverse('building-list')
    def test_func(self):
        building = self.get_object()
        if self.request.user == building.owner:
            return True
        return False

#+++++++++++++++ Unit CRUD ++++++++++++++++++++



class UnitListView(ListView):
    model = Unit
    template_name = 'unit_list.html'
    def get_queryset(self):
        return super().get_queryset().filter(building=self.kwargs['building_pk']) 

class UnitCreateView(CreateView):
    model = Unit
    fields = ['name','description','image','rent']
    success_message = "Unit created successfully!"

    def get_success_url(self):
        return reverse_lazy('unit-home', kwargs = {'building_pk': self.object.building.pk})
    
    def form_valid(self,form):
        form.instance.owner = self.request.user
        form.instance.building = self.building
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.building = get_object_or_404(Building, pk=kwargs['building_pk'])
        return super().dispatch(request, *args, **kwargs)
        
    def test_func(self):
        unit = self.get_object()
        if self.request.user == unit.building.owner:
            return True
        return False

class UnitDetailView(DetailView):
    template_name = 'units/unit_detail.html'
    model = Unit
    success_url = reverse_lazy('unit-detail')

class UnitUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Unit
    success_url = reverse_lazy('unit-detail')
    fields = ['name','description','image','rent']
    success_message = "Unit updated successfully!"
    
    def get_success_url(self):
        return reverse_lazy('unit-detail', kwargs = {'building_pk': self.object.building.pk})

    def test_func(self):
        unit = self.get_object()
        if self.request.user == unit.building.owner:
            return True
        return False

class UnitDeleteView(DeleteView):
    model= Unit
    success_message = "The Unit %(title) was deleted successfully!"

    def get_success_url(self):
        return reverse_lazy('unit-detail', kwargs = {'building_pk': self.object.building.pk})
