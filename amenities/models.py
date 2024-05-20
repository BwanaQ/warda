from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    amenity_type = models.CharField(max_length=100)
    point_location = models.PointField(null=True, blank=True)
    polygon_location = models.PolygonField(null=True, blank=True)
    geom_type = models.CharField(max_length=50)  # New field to store geometry type

    class Meta:
        verbose_name_plural = "Amenities"
    def __str__(self):
        return self.name