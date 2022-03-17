from django.contrib import admin

from .models import Category, Order, Post


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


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "price",
        "status",
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
