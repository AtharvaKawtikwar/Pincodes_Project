# Generated by Django 5.1.1 on 2024-09-30 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pincode_app', '0002_alter_pincode_latitude_alter_pincode_longitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nearbypincode',
            name='nearby_pincodes',
        ),
        migrations.AddField(
            model_name='nearbypincode',
            name='nearby_pincode',
            field=models.JSONField(null=True),
        ),
    ]
