from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    ListView,
    View
)
from .models import (
    Status,
    Application,
)

from .forms import *
class ApplicationCreateView(SuccessMessageMixin,CreateView):
    """Create view for Application"""
    model = Application
    fields = ['tenant','unit']
    template_name = 'applications/application_create.html'
    success_message = 'Application successfully created!'
    error_message = 'Error saving the Application, check fields below.'
    success_message = 'Application successfully created!'

    def post(self, request):
        pending, _ = Status.objects.get_or_create(name='Pending')
        form = ApproveApplicationForm(request.POST)
        # Check if unit already assigned and tenant cant book the same unit again
        # When leasing you can check the above not neccessary. add checks the same person cant apply again same unit
        if form.is_valid():
            cleaned_data = form.cleaned_data
            Application.objects.create(
                tenant=cleaned_data.get('tenant'),
                unit=cleaned_data.get('unit'),
                status=pending
            )
            messages.success(request, self.success_message)
            return redirect('application-list')
        else:
            messages.error(self.request, self.error_message)
            return render(request,template_name=self.template_name,context={'form': form})

class ApplicationUpdateView(SuccessMessageMixin,UpdateView):
    """Update view for Application"""
    model = Application
    fields = ['tenant','unit','status','date_approved','date_denied','date_cancelled','date_completed']
    template_name = 'applications/edit_application.html'
    success_message = 'Application successfully updated!'
    error_message = 'Error saving the Application, check fields below.'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('application-list')



"""Application Views"""
class ApplicationDeleteView(SuccessMessageMixin,DeleteView):
    """Delete view for Application"""
    model = Application
    template_name = 'confirm_delete.html'
    success_message = 'Application successfully deleted!'
    error_message = 'Error deleteing Application.'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(ApplicationDeleteView, self).post(request, *args, **kwargs)

    def get_object(self):
        id_ = self.kwargs.get('id')
        if not id_:
            messages.error(self.request, self.error_message)
        return get_object_or_404(Application, id=id_)

    def get_success_url(self):
        return reverse('application-list')


class ApplicationDetailView(DetailView):
    """Detail view for Application"""
    model = Application
    template_name = 'applications/application_detail.html'
    context_object_name = 'application'

    

class  ApplicationListView(ListView):
    """List view for Application"""
    model = Application
    context_object_name = 'application_list'   # your own name for the list as a template variable
    template_name = 'applications/application_list.html'

    def get_queryset(self):
        """Return all Application objects"""
        return Application.objects.all()

class ApproveApplicationView(SuccessMessageMixin, CreateView):
    template_name = 'applications/approve_application.html'
    model = Application
    fields = ['tenant', 'unit']
    error_message = "An error occured"
    def post(self, request):
        approved, _ = Status.objects.get_or_create(name='Approved')
        form = ApproveApplicationForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            messages.success(request, 'application approved!')
            return redirect('approve-application')

        else:
            messages.error(self.request, self.error_message)
            return render(request,template_name=self.template_name,context={'form': form})