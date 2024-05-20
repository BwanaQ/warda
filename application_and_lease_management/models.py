from django.db import models
from authentication.models import (
    TimeStampedModel,
    Tenant,
    Landlord,
    User
)

class Status(models.Model):
    """Represents a status of a lease e.g. Pending, Approved, etc"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class LeaseType(models.Model):
    """Represents a lease type"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class LeaseInfo(TimeStampedModel):
    """Represents unit lease information"""
    lease_type = models.ForeignKey(LeaseType, on_delete=models.CASCADE)
    is_sub_leasing_allowed = models.BooleanField(default=False)
    application_fee = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    is_lease_termination_allowed = models.BooleanField(default=False)
    lease_termination_cost = models.DecimalField(
        max_digits=10, decimal_places=2)
    lease_term = models.CharField(max_length=50)
    lease_term_in_months = models.IntegerField()
    additional_lease_clauses = models.TextField(blank=True, null=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    utilities_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    total_rent = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.lease_type.name


class Application(TimeStampedModel):
    """Represents a lease application"""
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )
    unit = models.ForeignKey(
        'portfolio.Unit',
        on_delete=models.CASCADE
    )
    status = models.ForeignKey(Status, on_delete=models.CASCADE,null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    date_approved = models.DateTimeField(blank=True, null=True)
    date_denied = models.DateTimeField(blank=True, null=True)
    date_cancelled = models.DateTimeField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.tenant} - {self.unit}'


class UnitLease(TimeStampedModel):
    """Represents a lease for a unit"""
    unit = models.ForeignKey(
        'portfolio.Unit',
        on_delete=models.CASCADE
    )
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)
    is_first_time = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f'{self.unit} - {self.application}'
