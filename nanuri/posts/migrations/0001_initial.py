# Generated by Django 3.2.12 on 2022-03-17 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='uuid')),
                ('title', models.CharField(max_length=255)),
                ('image_url', models.URLField()),
                ('unit_price', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('min_participants', models.PositiveIntegerField()),
                ('max_participants', models.PositiveIntegerField()),
                ('num_participants', models.PositiveIntegerField(default=0)),
                ('product_url', models.URLField()),
                ('trade_type', models.CharField(blank=True, choices=[('DIRECT', '직거래'), ('PARCEL', '택배 거래')], max_length=15, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.category')),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('ADVERTISING', '인원 모집 중'), ('ORDERED', '주문 완료'), ('DELIVERING1', '1차 배송 중'), ('DELIVERING2', '2차 배송 중'), ('DELIVERED', '배송 완료'), ('CANCELLED', '취소됨')], default='ADVERTISING', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
    ]
