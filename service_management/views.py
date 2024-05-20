from django.shortcuts import render,reverse,redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import (
View,
ListView,
DetailView,
UpdateView,
CreateView
)

from .models import (
ServiceRequest,
ServiceCategory,
ServiceRequestProposal
)
from portfolio.models import (
Building,
Unit
)

from service_management.forms import (
ServiceRequestForm,
ServiceRequestProposalForm
)
from application_and_lease_management.models import Status
from authentication.models import (
    ServicePRO
)

from authentication.models import (
    User
)

class UnitMaintainanceRequestView(View):
    template_name = 'service_requests/form_request.html'
    # model = ServiceRequest

    def get(self, request,building_pk,unit_pk):
        form = ServiceRequestForm()
        building = Building.objects.get(id=building_pk)
        unit = Unit.objects.get(id=unit_pk)
        context = {'form': form, 'building': building,'unit':unit}
        return render(request, self.template_name, context)

    def post(self,request,building_pk, unit_pk):
        form = ServiceRequestForm(request.POST)
        building = Building.objects.get(id=building_pk)
        unit = Unit.objects.get(id=unit_pk)
        category = ServiceCategory.objects.get(id=request.POST.get('service_category'))
        status, _ = Status.objects.get_or_create(name='Pending')
        request_by = User.objects.get(email=request.user)
        try:
            if form.is_valid():
                cleaned_data = form.cleaned_data
                ServiceRequest.objects.create(
                    unit = unit,
                    status = status,
                    service_category = category,
                    description = cleaned_data.get('description'),
                    requested_by =request_by
                )

                messages.success(request, 'Service Request sent successfully!')
                return redirect('service-requests')

            else:
                messages.error(self.request, self.error_message)
                return render(request,template_name=self.template_name,context={'form': form})
        except Exception as e:
            messages.error(self.request, str(e))
            return render(request,template_name=self.template_name,context={'form': form})




class ServiceRequestListView(ListView):
    template_name = 'service_requests/service_request_list.html'
    model = ServiceRequest
    context_object_name = 'service_request_list'   # your own name for the list as a template variable

    def get_queryset(self):
        """Return all Amenity objects"""
        return ServiceRequest.objects.all()


class ServiceCategoryListView(ListView):
    template_name = 'service_categories/service_category_list.html'
    model = ServiceCategory
    context_object_name = 'service_category_list'   # your own name for the list as a template variable

    def get_queryset(self):
        """Return all Amenity objects"""
        return ServiceCategory.objects.all()


class ServicePROJobsListView(ListView):
    template_name = 'service_requests/service_pro_jobs.html'
    model = ServiceRequest
    context_object_name = 'job_list'   # your own name for the list as a template variable

    def get_queryset(self):
        """Return all Amenity objects"""
        return ServiceRequest.objects.filter(status__name='Pending')


class ServiceRequestDetailView(DetailView):
    template_name = 'service_requests/service_request_detail.html'
    model = ServiceRequest
    context_object_name = 'job' 
    fields = ['subject','description']
    def get(self, request,pk):
        form = ServiceRequestProposalForm()
        service_request = ServiceRequest.objects.get(id=pk)
        context = {'form': form, 'service_request': service_request}
        return render(request, self.template_name, context)

class CreateProposalView(CreateView):
    template_name = 'service_requests/proposal_form.html'
    model = ServiceRequest

    def get(self, request,pk):
        form = ServiceRequestProposalForm()
        service_request = ServiceRequest.objects.get(id=pk)
        unit = service_request.unit
        context = {'form': form, 'service_request': service_request, 'unit': unit}
        return render(request, self.template_name, context)

    def post(self,request,pk):
        form = ServiceRequestProposalForm(request.POST)

        try:
            service_request = ServiceRequest.objects.get(id=pk)

            service_pro = ServicePRO.objects.get(user__email=request.user)

            if form.is_valid():
                cleaned_data = form.cleaned_data
            
                ServiceRequestProposal.objects.create(
                    service_request = service_request,
                    service_pro =service_pro,
                    status='Pending',
                    description = cleaned_data.get('description')
                )
                service_request.total_proposals+=1
                service_request.save()
                messages.success(request, 'Proposal sent successfully!')
                return redirect('service-pro-jobs')

            else:
                messages.error(self.request, self.error_message)
                return render(request,template_name=self.template_name,context={'form': form})
        except Exception as e:
                messages.error(self.request, str(e))
                return render(request,template_name=self.template_name,context={'form': form})


class ServicePROProposalListView(ListView):
    template_name = 'service_pro/proposals.html'
    model = ServiceRequest
    context_object_name = 'proposal_list'
    def get_queryset(self):
        """Return all service proposals for specific service pro"""
        try:
            service_pro = ServicePRO.objects.get(user__email=self.request.user)
            return ServiceRequestProposal.objects.filter(service_pro=service_pro)
        except Exception as e:
            messages.error(self.request, str(e))
            return render(self.request,template_name=self.template_name,context={'form': None})


