from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    Role,
    User,
    
    
)

class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'role_type', 'is_staff', 'is_active')
    list_filter = ('email', 'role_type', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('phone_number','email', 'first_name','last_name','role_type', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','phone_number','email', 'role_type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'role_type',)
    ordering = ('email', 'role_type',)


admin.site.register(User, UserAdmin)