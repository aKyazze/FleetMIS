# Generated by Django 4.2.11 on 2024-11-27 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleetApp', '0005_requestor_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='status',
            field=models.CharField(choices=[('Av', 'Available'), ('Al', 'Allocated')], max_length=2),
        ),
    ]
