from django.contrib import admin

from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'title',
        'image_url',
        'unit_price',
        'quantity',
        'description',
        'min_participants',
        'max_participants',
        'num_participants',
        'product_url',
        'trade_type',
        'order_status',
        'is_published',
        'published_at',
        'created_at',
        'updated_at',
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "parent",
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
