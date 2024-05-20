from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth import (
    password_validation,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from django.db.models import Q
from .models import *

from django import forms

from locations.models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'role_type')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


class RoleForm(forms.Form):
    class Meta:
        model = Role
        fields = ('name')


class RegisterForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField()
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('first_name','last_name','email','phone','password1','password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

class RegisterWithRoleSelectForm(forms.ModelForm):
    ROLE_CHOICES = (
        (1, 'Landlord'),
        (2, 'Tenant'),
        (3, 'Service PRO')
    )
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    role_type = forms.ModelChoiceField(queryset=Role.objects.filter(
        Q(name='Tenant')|
        Q(name='Landlord')|
        Q(name = 'Service PRO')
    ))
    email = forms.EmailField()
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('first_name','last_name','email','phone','password1','password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)










class TenantIdentityForm(forms.Form):
    IDENTIFICATION_TYPE_CHOICES = (
        (1, 'Passport'),
        (2, 'National ID'),
        (3, 'Birth Certificate')
    )

    identification_type = forms.Select(choices=IDENTIFICATION_TYPE_CHOICES)
    id_no = forms.CharField(max_length=100)


class TenantAddressForm(forms.Form):
    county = forms.ModelChoiceField(queryset=County.objects.all())
    city = forms.CharField(max_length=100)


class TenantEmploymentForm(forms.Form):
    INCOME_CHOICES = (
        (1, 'below 20,0000 ksh'),
        (2, '20,000-50,000 ksh'),
        (3, '50,000-100,000 ksh'),
        (4, 'above 100,000 ksh')
    )
    job_title = forms.CharField(max_length=100)
    income = forms.Select(choices=INCOME_CHOICES)


class TenantNextOfKinForm(forms.ModelForm):
    RELATION_CHOICEs = (
        (1, 'Mother'),
        (2, 'Father'),
        (3, 'Sister'),
        (4, 'Brother'),
        (5, 'Wife'),
        (6, 'Husband')
    )
    # TODO to be used for rent  application
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    relation = forms.Select(choices=RELATION_CHOICEs)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField()

