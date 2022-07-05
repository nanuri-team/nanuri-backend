from django.contrib import admin

from .models import Category, Comment, Post, PostImage, SubComment


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'title',
        'writer',
        'writer_address',
        'writer_nickname',
        'image',
        'category',
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

    def writer_address(self, obj):
        return obj.writer.address

    def writer_nickname(self, obj):
        return obj.writer.nickname


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


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "post",
        "text",
        "writer",
    ]


class SubCommentAdmin(admin.ModelAdmin):
    list_display = [
        "comment",
        "text",
        "writer",
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SubComment, SubCommentAdmin)
