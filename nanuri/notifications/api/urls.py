from django.urls import path

from . import views

app_name = "nanuri.notifications.api"

urlpatterns = [
    path(
        "devices/",
        view=views.DeviceCreateAPIView.as_view(),
        name="device-list",
    ),
    path(
        "devices/<uuid:uuid>/",
        view=views.DeviceRetrieveUpdateDestroyAPIView.as_view(),
        name="device-detail",
    ),
    path(
        "devices/<uuid:device_uuid>/subscriptions/",
        view=views.SubscriptionListCreateAPIView.as_view(),
        name="subscription-list",
    ),
    path(
        "devices/<uuid:device_uuid>/subscriptions/<uuid:uuid>/",
        view=views.SubscriptionRetrieveDestroyAPIView.as_view(),
        name="subscription-detail",
    ),
]
