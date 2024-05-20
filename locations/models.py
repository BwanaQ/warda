from django.contrib.gis.db import models
class Country(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.name
class County(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.name
class SubCounty(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    county = models.ForeignKey(County,on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.name
class Ward(models.Model):
    name = models.CharField(max_length=100)
    subcounty = models.ForeignKey(SubCounty,on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.name

class Town(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.name

class ZipCode(models.Model):
    code = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.no

class StreetAddress(models.Model):
    address = models.CharField(max_length=200,blank=True, null=True)
    def __str__(self):
        return self.address

class Address(models.Model):
    """Represents a physical address"""
    street_address = models.ForeignKey(StreetAddress,on_delete=models.CASCADE,null=True,blank=True,related_name="streets")
    city = models.ForeignKey(City,on_delete=models.CASCADE,null=True,blank=True)
    town = models.ForeignKey(Town,on_delete=models.CASCADE,null=True,blank=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    zip_code = models.ForeignKey(ZipCode,on_delete=models.CASCADE,null=True,blank=True)
    county = models.ForeignKey(County,on_delete=models.CASCADE,null=True,blank=True,related_name="counties")
    subcounty = models.ForeignKey(SubCounty,on_delete=models.CASCADE,null=True,blank=True,related_name="subcounties")
    ward = models.ForeignKey(SubCounty,on_delete=models.CASCADE,null=True,blank=True,related_name="wards")
    country = models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True,related_name="countries")
    coords = models.PointField(blank=True, null=True, srid=4326, )

    def __str__(self):
        return self.street_address.address