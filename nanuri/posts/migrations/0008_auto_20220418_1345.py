# Generated by Django 3.2.13 on 2022-04-18 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_alter_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='waited_from',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='waited_until',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
