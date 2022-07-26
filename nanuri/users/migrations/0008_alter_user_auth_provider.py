# Generated by Django 3.2.13 on 2022-07-25 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_favorite_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth_provider',
            field=models.CharField(blank=True, choices=[('APPLE', '애플'), ('KAKAO', '카카오')], max_length=15, null=True),
        ),
    ]
