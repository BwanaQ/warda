from django.contrib import admin
from .models import (
    ServiceCategory,
    ServiceRequest,
    ServiceRequestProposal
)

admin.site.register(ServiceCategory)
admin.site.register(ServiceRequestProposal)

@admin.register(ServiceRequest)
class Servicedmin(admin.ModelAdmin):
    list_display =  (
        'id',
        'unit',
        'service_category',
        'description',
        'assinged_to',
        'total_proposals',
        'created',
        'modified'

    
    )
    
    search_fields = (
        'service_category',
        'assigned_to',
    )
