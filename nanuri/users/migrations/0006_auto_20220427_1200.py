# Generated by Django 3.2.13 on 2022-04-27 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_url',
        ),
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]
