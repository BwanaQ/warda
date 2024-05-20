from django.contrib import admin
from .models import Invoice



@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display =  (
        'id',
        'invoice_no',
        'unitlease',
        'description',
        'month',
        'amount',
        'date_paid',
        'date_due',
        'paid'
    
    )
    
    search_fields = (
        'month',
        'paid',
    )


