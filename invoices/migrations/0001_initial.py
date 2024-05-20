# Generated by Django 5.0.4 on 2024-05-20 07:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('application_and_lease_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('invoice_no', models.CharField(blank=True, max_length=255, null=True)),
                ('month', models.IntegerField(blank=True, null=True)),
                ('date_paid', models.DateTimeField(blank=True, null=True)),
                ('date_due', models.DateField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('building_id', models.BigIntegerField(blank=True, null=True)),
                ('unitlease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_and_lease_management.unitlease')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
