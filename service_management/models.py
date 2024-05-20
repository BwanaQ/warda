from django.db import models

from authentication.models import (
    Landlord,
    TimeStampedModel,
    User,
    ServicePRO
)
from application_and_lease_management.models import Status

class ServiceCategory(models.Model):
    """Represents a category of services e.g. Cleaning, Plumbing, etc"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.name

class ServiceRequest(TimeStampedModel):
    """Represents a service request e.g. Cleaning, Plumbing, etc"""
    unit = models.ForeignKey('portfolio.Unit', on_delete=models.CASCADE)
    subject = models.CharField(max_length=250, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    assinged_to = models.ForeignKey(ServicePRO, on_delete=models.CASCADE,null=True, blank=True)
    date_resolved = models.DateTimeField(null=True, blank=True)
    total_proposals = models.BigIntegerField(default=0)
    requested_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        if  self.service_category is None:
            return 'N/A'
        return self.service_category.name

class ServiceRequestProposal(TimeStampedModel):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    )
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    service_pro = models.ForeignKey(ServicePRO, on_delete=models.CASCADE, null=True,blank=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,null=True,blank=True)



    # def __str__(self):
    #     return self.service_request.subject