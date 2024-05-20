from django.core.management.base import BaseCommand
import geopandas as gpd
from django.contrib.gis.geos import Point, Polygon, LinearRing, GEOSGeometry  # Import LinearRing
from amenities.models import Amenity
from shapely.geometry import shape, Polygon, LinearRing

class Command(BaseCommand):
    help = 'Populates amenities from an OSM GeoJSON file'

    def add_arguments(self, parser):
        parser.add_argument('geojson_file', type=str, help='Path to the OSM GeoJSON file')

    def handle(self, *args, **kwargs):
        geojson_file = kwargs['geojson_file']

        # Delete all existing records and print the count of records deleted
        deleted_count, _ = Amenity.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'{deleted_count} records deleted.'))

        # Load the GeoJSON file
        gdf = gpd.read_file(geojson_file)

        # Filter amenities with name, amenity_type, and supported geometry types (Point and Polygon)
        filtered_amenities = gdf[(gdf['amenity'].notnull()) & (gdf['name'].notnull()) & ((gdf.geometry.type == 'Point') | (gdf.geometry.type == 'Polygon'))]

        # Iterate over filtered amenities and save to Django model
        for idx, row in filtered_amenities.iterrows():
            geom_type = row.geometry.geom_type

            if geom_type == 'Point':
                try:
                    # Create a Point object from the geometry coordinates
                    point = Point(row.geometry.x, row.geometry.y)

                    # Create or update the Amenity model instance
                    amenity, created = Amenity.objects.get_or_create(
                        name=row['name'],
                        amenity_type=row['amenity'],
                        geom_type=geom_type  # Save the geometry type
                    )
                    amenity.point_location = point

                    # Save the Amenity instance
                    amenity.save()

                    # Print a message for each record inserted
                    self.stdout.write(self.style.SUCCESS(f'Record "{row["name"]}" inserted.'))

                except Exception as e:
                    # Log the error and continue to the next row
                    self.stdout.write(self.style.ERROR(f'Error inserting amenity "{row["name"]}": {e}'))
                    continue



            elif geom_type == 'Polygon':
                try:
                    # Extract the exterior ring coordinates from the GeoJSON structure
                    exterior_ring_coords = row.geometry.exterior.coords

                    # Convert the exterior ring coordinates to a list of tuples
                    exterior_ring_coords = [(x, y) for x, y in exterior_ring_coords]

                    # Create a LinearRing object for the exterior ring
                    exterior_ring = LinearRing(exterior_ring_coords)

                    # Create a Polygon object using the exterior ring
                    polygon = Polygon(exterior_ring)

                    # Convert the Polygon object to a GEOSGeometry object
                    geos_polygon = GEOSGeometry(polygon.wkt)

                    # Create or update the Amenity model instance
                    amenity, created = Amenity.objects.get_or_create(
                        name=row['name'],
                        amenity_type=row['amenity'],
                        geom_type=geom_type,  # Save the geometry type
                        polygon_location=geos_polygon  # Set the polygon location
                    )

                    # Print a message for each record inserted
                    self.stdout.write(self.style.SUCCESS(f'Record "{row["name"]}" inserted.'))

                except Exception as e:
                    # Log the error and continue to the next row
                    self.stdout.write(self.style.ERROR(f'Error inserting amenity "{row["name"]}": {e}'))
                    continue
                    
        
        self.stdout.write(self.style.SUCCESS('Amenities population completed.'))
