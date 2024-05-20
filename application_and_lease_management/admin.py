from django.contrib import admin
from .models import (
    Status,
    LeaseType,
    LeaseInfo,
    Application,
    UnitLease
)

admin.site.register(Status)
admin.site.register(LeaseType)
admin.site.register(LeaseInfo)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display =  (
        'id',
        'tenant',
        'unit',
        'status',
        'staff'
    
    )
    
    search_fields = (
        'tenant',
        'unit',
    )

@admin.register(UnitLease)
class UnitLeaseAdmin(admin.ModelAdmin):
    list_display =  (
        'id',
        'unit',
        'application',
        'is_active',
        'is_first_time',
        'start_date',
        'end_date',
        'rent',
        'deposit',
        'balance',
        'created',
        'modified'
    
    )
    
    search_fields = (
        'is_first_time',
        'is_active',
        'unit',
    )