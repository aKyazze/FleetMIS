# Generated by Django 4.2.11 on 2025-05-27 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleetApp', '0002_alter_driver_user_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='request_status',
            field=models.CharField(choices=[('P', 'Pending'), ('O', 'Open'), ('R', 'Rejected'), ('C', 'Closed')], default='P', max_length=1),
        ),
    ]
