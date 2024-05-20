from django.db import models
from authentication.models import (
    TimeStampedModel
)

class NotificationType(models.Model):
    """Represents a type of notification e.g. Lease Application, Service Request, Payments etc"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Notification(TimeStampedModel):
    """Represents a notification e.g. Lease Application, Service Request, Payments etc"""
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField()
    date_resolved = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.notification_type
