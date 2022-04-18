from django.contrib import admin

from .models import Category, Post, PostImage


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'title',
        'image',
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
        'waited_from',
        'waited_until',
        'created_at',
        'updated_at',
    ]


class PostImageAdmin(admin.ModelAdmin):
    list_display = [
        "post",
        "image",
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "parent",
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(Category, CategoryAdmin)
