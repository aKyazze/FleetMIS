# Generated by Django 4.2.11 on 2024-11-24 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleetApp', '0003_alter_driver_gender_alter_vehicle_engine_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Requisition',
        ),
    ]