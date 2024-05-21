from django.contrib.gis.db import models
from django.urls.base import reverse
from authentication.models import (
    TimeStampedModel,
    User,
    Landlord
)
from application_and_lease_management.models import (
    LeaseInfo,
)

from locations.models import (
    Address
)

     

class Community(models.Model):
    """Represents a neighbourhood or community area e.g Nyayo Estate"""
    name = models.CharField(max_length=255,null=True,blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('community_detail', kwargs={'pk': self.pk})

class Amenity(models.Model):
    """Represents a community area e.g parking,gym,pool,etc"""
    name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('amenities_detail', kwargs={'pk': self.pk})


class NeighbourType(models.Model):
    """Represents a neighbourhood type e.g School, Gym, Supermarket etc"""
    name = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('neighbour_type_detail', kwargs={'pk': self.pk})


class Neighbour(models.Model):
    """Represents neighbours around the building area e.g schools,hospitals, etc"""
    name = models.CharField(max_length=255,null=True,blank=True)
    category = models.ForeignKey(NeighbourType, on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField(blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('neighbour_detail', kwargs={'pk': self.pk})


class BuildingFeature(models.Model):
    """Represents a building feature"""
    name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Building(TimeStampedModel):
    """Represents a building
    TODO : Add created by for db audits
    """
    name = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(
        upload_to='warda_monolith/', blank=True, null=True)
    description = models.TextField()
    location = models.PointField(blank=True, null=True, srid=4326, )
    has_parking = models.BooleanField(default=False)
    has_parking_description = models.TextField(blank=True, null=True)
    has_elevator = models.BooleanField(default=False)
    has_garden = models.BooleanField(default=False)
    has_swimming_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_play_area = models.BooleanField(default=False)
    has_play_area_description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        User, related_name='buildings', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UnitType(models.Model):
    """Represents a type of unit e.g. studio,bed sitter,furnished  etc"""
    name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name


class UnitFeature(models.Model):
    """Represents unit features e.g. kitchen details etc"""
    name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='units/', blank=True, null=True)

    def __str__(self):
        return self.name


class Unit(TimeStampedModel):
    """Represents a single unit"""
    name = models.CharField(max_length=100,null=True,blank=True)
    unit_no = models.CharField(max_length=100, blank=True, null=True)
    unit_type = models.ForeignKey(UnitType, on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(
        upload_to='musonge/', blank=True, null=True)
    rent = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    is_occupied = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)
    unit_available_from = models.DateField(blank=True, null=True)
    no_of_bedrooms = models.IntegerField(default=0)
    no_of_bathrooms = models.IntegerField(default=0)
    no_of_toilets = models.IntegerField(default=0)
    no_of_balconies = models.IntegerField(default=0)
    unit_at_floor = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name='unit_likes')
    building = models.ForeignKey(
        Building, related_name='units', on_delete=models.CASCADE,null=True,blank=True)
    lease_info = models.ForeignKey(LeaseInfo, on_delete=models.CASCADE,null=True,blank=True)
    features = models.ManyToManyField(UnitFeature,blank=True)

    def __str__(self):
        return self.name

    def get_like_url(self):
        return reverse('listings:unit-like-toggle', kwargs={'pk': self.pk})
