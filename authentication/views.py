from django.contrib.auth import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic
from authentication.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .models import (
    Role,
    User,
    Agent,
    Landlord,
    Tenant
)


class Login(LoginView,SuccessMessageMixin):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_message = 'User successfully logged in!'
    error_message = 'Error logging in, check fields below.'

    def get_success_url(self):
        return reverse_lazy('dashboard')

class SignUp(generic.CreateView):
    form_class = RegisterWithRoleSelectForm
    template_name = 'signup.html'

    def post(self, request):
        form =RegisterWithRoleSelectForm(request.POST)

        try:
            if form.is_valid():
                cleaned_data = form.cleaned_data
                role_name = cleaned_data.get('role_type').name
                user = User.objects.create(
                    role_type = cleaned_data.get('role_type'),
                    username= cleaned_data.get('phone'),
                    email = cleaned_data.get('email'),
                    first_name=cleaned_data.get('first_name'),
                    last_name=cleaned_data.get('last_name')
                )

                grp ,_ = Group.objects.get_or_create(name=role_name)
                user.groups.add(grp)
                user.set_password(cleaned_data.get('password1'))
                user.save()
                if role_name == 'Tenant':
                    Tenant.objects.create(user=user)
                elif role_name == 'Landlord':
                    Landlord.objects.create(user=user)
                elif role_name == 'Service PRO':
                    ServicePRO.objects.create(user=user)
                else:
                    pass
                messages.success(request, 'registration success!')
                return redirect('login')
            messages.error(self.request,str(form.errors))
            return render(request,template_name=self.template_name,context={'form': form})
        except Exception as e:
            messages.error(self.request,str(e))
            return render(request,template_name=self.template_name,context={'form': form})




class ForgotPassword(View):
    template_name = 'forgot-password.html'

    def get(self, request, *args, **kwargs):
        return render(request,template_name=self.template_name,context={})
class Pricing(View):

    template_name = 'pricing.html'

    def get(self, request, *args, **kwargs):
        return render(request,template_name=self.template_name,context={})


class UserListView(generic.ListView):
    model = User
    context_object_name = 'user_list'   # your own name for the list as a template variable
    template_name = 'users/user_list.html'

    def get_queryset(self):
        """TODO filter by """
        return User.objects.all()


class AgentListView(generic.ListView):
    model = Agent
    context_object_name = 'agent_list'
    template_name = 'agents/agent_list.html'

    def get_queryset(self):
        """TODO filter by"""
        return Agent.objects.all()

class LandlordListView(generic.ListView):
    model = Landlord
    context_object_name = 'landlord_list'
    template_name = 'landlords/landlord_list.html'

    def get_queryset(self):
        """TODO filter by"""
        return Landlord.objects.all()

class TenantListView(generic.ListView):
    model = Tenant
    context_object_name = 'tenant_list'
    template_name = 'tenants/tenant_list.html'

    def get_queryset(self):
        """TODO filter by"""
        return Tenant.objects.all()



class LandlordSignUp(generic.CreateView):
    form_class = RegisterForm
    template_name = 'landlord/register.html'
    # TODO validate if username already exists 

    def post(self, request):
        role, _ = Role.objects.get_or_create(name='Landlord')
        group,_ = Group.objects.get_or_create(name='Landlord')
        form =RegisterForm(request.POST)

        try:
            if form.is_valid():
                cleaned_data = form.cleaned_data
                user = User.objects.create(
                    role_type = role,
                    username= cleaned_data.get('phone'),
                    email = cleaned_data.get('email'),
                    first_name=cleaned_data.get('first_name'),
                    last_name=cleaned_data.get('last_name')
                )
                user.groups.add(group)
                user.set_password(cleaned_data.get('password1'))
                user.save()
                Landlord.objects.create(
                    user=user
                )
                messages.success(request, 'registration success!')
                return redirect('login')
            messages.error(self.request,str(form.errors))
            return render(request,template_name=self.template_name,context={'form': form})
        except Exception as e:
            messages.error(self.request,str(e))
            return render(request,template_name=self.template_name,context={'form': form})

class TenantSignUp(generic.CreateView):
    """
    A viewthat creates a tenant, with no privileges, from the given phone and
    password.
    """
    # TODO validate if username already exists 
    form_class = RegisterForm
    template_name = 'tenant/register.html'

    def post(self, request):
        role, _ = Role.objects.get_or_create(name='Tenant')
        group,_ = Group.objects.get_or_create(name='Tenant')
        form =RegisterForm(request.POST)

        try:
            if form.is_valid():
                cleaned_data = form.cleaned_data
                user = User.objects.create(
                    role_type = role,
                    username= cleaned_data.get('phone'),
                    email = cleaned_data.get('email'),
                    first_name=cleaned_data.get('first_name'),
                    last_name=cleaned_data.get('last_name')
                )
                user.groups.add(group)
                user.set_password(cleaned_data.get('password1'))
                user.save()
                tenant = Tenant.objects.create(
                    user=user
                )
                messages.success(request, 'registration success!')
                return redirect('login')
            messages.error(self.request,str(form.errors))
            return render(request,template_name=self.template_name,context={'form': form})
        except Exception as e:
            messages.error(self.request,str(e))
            return render(request,template_name=self.template_name,context={'form': form})


class ServicePROSignUp(generic.CreateView):
    form_class = RegisterForm
    template_name = 'service_pro/register.html'

    def post(self, request):
        role, _ = Role.objects.get_or_create(name='Service PRO')
        group,_ = Group.objects.get_or_create(name='Service PRO')
        form = RegisterForm(request.POST)

        try:
            if form.is_valid():
                cleaned_data = form.cleaned_data
                user = User.objects.create(
                    role_type = role,
                    username= cleaned_data.get('phone'),
                    email = cleaned_data.get('email'),
                    first_name=cleaned_data.get('first_name'),
                    last_name=cleaned_data.get('last_name')
                )
                user.groups.add(group)
                user.set_password(cleaned_data.get('password1'))
                user.save()
                ServicePRO.objects.create(
                    user=user
                )
                messages.success(request, 'registration success!')
                return redirect('login')
            messages.error(self.request,str(form.errors))
            return render(request,template_name=self.template_name,context={'form': form})
        except Exception as e:
            messages.error(self.request,str(e))
            return render(request,template_name=self.template_name,context={'form': form})