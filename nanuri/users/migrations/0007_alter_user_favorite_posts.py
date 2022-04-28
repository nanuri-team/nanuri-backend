# Generated by Django 3.2.13 on 2022-04-28 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20220420_1512'),
        ('users', '0006_auto_20220427_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favorite_posts',
            field=models.ManyToManyField(blank=True, related_name='favored_by', to='posts.Post'),
        ),
    ]
