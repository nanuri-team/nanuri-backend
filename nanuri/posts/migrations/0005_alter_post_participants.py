# Generated by Django 3.2.13 on 2022-04-12 14:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_auto_20220412_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='posts_participated', to=settings.AUTH_USER_MODEL),
        ),
    ]
