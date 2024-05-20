from django.db import models
from application_and_lease_management.models import UnitLease
from authentication.models import (
    TimeStampedModel
)

class Invoice(TimeStampedModel):
    """Represents an invoice"""
    unitlease = models.ForeignKey(UnitLease, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=255, blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    date_paid = models.DateTimeField(blank=True, null=True)
    date_due = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    building_id = models.BigIntegerField(null=True,blank=True)

    def __str__(self):
        return self.unitlease.unit.name


