from django.core.management.base import BaseCommand
from amenities.models import Amenity

class Command(BaseCommand):
    help = 'Deletes amenities with the name "Homestead"'

    def handle(self, *args, **kwargs):
        # Delete amenities with name "Homestead"
        deleted_count, _ = Amenity.objects.filter(name="Homestead").delete()
        self.stdout.write(self.style.SUCCESS(f'{deleted_count} amenities named "Homestead" deleted.'))