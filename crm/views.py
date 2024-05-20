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
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from .models import (
    Lead
)
class ContactView(SuccessMessageMixin,CreateView):
    """Create contact view"""
    model = Lead
    fields = ['first_name','last_name','email','phone','message']
    template_name = 'contacts/contact.html'
    success_message = 'You have successfully sent the message. We will respond, as soon as possible!'
    error_message = 'Error sending the message, check fields below.'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('/')

class ContactCreateView(SuccessMessageMixin,CreateView):
    """Create contact view"""
    model = Lead
    fields = ['first_name','last_name','email','phone','message','source']
    template_name = 'contacts/contact_create.html'
    success_message = 'You have successfully sent the message. We will respond, as soon as possible!'
    error_message = 'Error sending the message, check fields below.'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('/')


class ContactUpdateView(SuccessMessageMixin,UpdateView):
    """Update view for Contact"""
    model = Lead
    fields = ['first_name','last_name','email','phone','message','source']
    template_name = 'contacts/edit_contact.html'
    success_message = 'Contact successfully updated!'
    error_message = 'Error saving the Contact, check fields below.'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('contact-list')

class ContactDeleteView(SuccessMessageMixin,DeleteView):
    """Delete view for Contact"""
    model = Lead
    template_name = 'confirm_delete.html'
    success_message = 'Contact successfully deleted!'
    error_message = 'Error deleteing Contact.'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(ContactDeleteView, self).post(request, *args, **kwargs)

    def get_object(self):
        id_ = self.kwargs.get('id')
        if not id_:
            messages.error(self.request, self.error_message)
        return get_object_or_404(Lead, id=id_)

    def get_success_url(self):
        return reverse('contact-list')


class ContactDetailView(DetailView):
    """Detail view for Contact"""
    model = Lead
    template_name = 'contacts/contact_detail.html'
    context_object_name = 'contact'

    

class  ContactListView(ListView):
    """List view for Contact"""
    model = Lead
    context_object_name = 'contact_list'   # your own name for the list as a template variable
    template_name = 'contacts/contact_list.html'

    def get_queryset(self):
        """Return all Contact objects"""
        return Lead.objects.all()