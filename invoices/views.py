from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    ListView,
)
from .models import (
    Invoice
)
class InvoiceCreateView(SuccessMessageMixin,CreateView):
    """Create invoice view"""
    model = Invoice
    fields = ['unitlease','invoice_no','month','date_paid','date_due','amount','description','paid']
    template_name = 'invoices/invoice_create.html'
    success_message = 'You have successfully sent the message. We will respond, as soon as possible!'
    error_message = 'Error sending the message, check fields below.'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('/')


class InvoiceUpdateView(SuccessMessageMixin,UpdateView):
    """Update view for Invoice"""
    model = Invoice
    fields = ['unitlease','invoice_no','month','date_paid','date_due','amount','description','paid']
    template_name = 'invoices/edit_invoice.html'
    success_message = 'Invoice successfully updated!'
    error_message = 'Error saving the Invoice, check fields below.'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('invoice-list')

class InvoiceDeleteView(SuccessMessageMixin,DeleteView):
    """Delete view for Invoice"""
    model = Invoice
    template_name = 'confirm_delete.html'
    success_message = 'Invoice successfully deleted!'
    error_message = 'Error deleteing Invoice.'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(InvoiceDeleteView, self).post(request, *args, **kwargs)

    def get_object(self):
        id_ = self.kwargs.get('id')
        if not id_:
            messages.error(self.request, self.error_message)
        return get_object_or_404(Invoice, id=id_)

    def get_success_url(self):
        return reverse('invoice-list')


class InvoiceDetailView(DetailView):
    """Detail view for Invoice"""
    model = Invoice
    template_name = 'invoices/invoice_detail.html'
    context_object_name = 'invoice'

    

class  InvoiceListView(ListView):
    """List view for Invoice"""
    model = Invoice
    context_object_name = 'invoice_list'   # your own name for the list as a template variable
    template_name = 'invoices/invoice_list.html'

    def get_queryset(self):
        """Return all Invoice objects"""
        return Invoice.objects.all()