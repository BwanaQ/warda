from django.db import models


class LeadSource(models.Model):
    """Represent a source of a lead"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Lead(models.Model):
    """Represents a lead in the CRM."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    source = models.ForeignKey(LeadSource, on_delete=models.CASCADE)
    is_phoned = models.BooleanField(default=False)
    is_converted_to_customer = models.BooleanField(default=False)
    date_converted_to_customer = models.DateField(null=True, blank=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='leads', null=True,blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} - {self.user.last_name} - {self.message}'

