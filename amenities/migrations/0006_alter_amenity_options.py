# Generated by Django 5.0.4 on 2024-05-18 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amenities', '0005_alter_amenity_options_amenity_geom_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amenity',
            options={'verbose_name_plural': 'Amenities'},
        ),
    ]
