# Generated by Django 3.2.15 on 2022-09-05 07:24

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_alter_subscription_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]
