from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # Add other fields as necessary

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    location = models.PointField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='buildings')
    # Add other fields as necessary

    class Meta:
        verbose_name_plural = "Buildings"

    def __str__(self):
        return self.name
    
class Unit(models.Model):
    name = models.CharField(max_length=100)
    rent_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='units')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='units')
    # Add other fields as necessary

    def __str__(self):
        return self.name    