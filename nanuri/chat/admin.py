from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'message',
        'room_name',
        'sender',
        'sent_at',
    ]
    list_filter = [
        'room_name',
    ]


admin.site.register(Message, MessageAdmin)
