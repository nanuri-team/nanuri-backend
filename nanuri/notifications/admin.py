from django import forms
from django.contrib import admin

from .models import Device, Subscription


class DeviceChangeForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ("user", "device_token", "opt_in", "endpoint_arn")


class DeviceAdmin(admin.ModelAdmin):
    form = DeviceChangeForm
    list_display = [
        "uuid",
        "user",
        "device_token",
        "opt_in",
        "endpoint_arn",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ("endpoint_arn",)


class SubscriptionChangeForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ("device", "topic", "group_code", "opt_in", "subscription_arn")


class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionChangeForm
    list_display = [
        "uuid",
        "device",
        "topic",
        "group_code",
        "opt_in",
        "subscription_arn",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ("subscription_arn",)


admin.site.register(Device, DeviceAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
