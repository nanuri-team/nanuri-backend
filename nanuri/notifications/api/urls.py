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
        "subscriptions/",
        view=views.SubscriptionListCreateAPIView.as_view(),
        name="subscription-list",
    ),
    path(
        "subscriptions/<uuid:uuid>/",
        view=views.SubscriptionRetrieveUpdateDestroyAPIView.as_view(),
        name="subscription-detail",
    ),
]
