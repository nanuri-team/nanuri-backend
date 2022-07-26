import factory
from factory.django import DjangoModelFactory

from nanuri.notifications.models import Device, Subscription

from ..posts.factories import PostFactory
from ..users.factories import UserFactory


class DeviceFactory(DjangoModelFactory):
    class Meta:
        model = Device

    user = factory.SubFactory(UserFactory)
    device_token = factory.Faker("pystr", min_chars=64, max_chars=152)


class SubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = Subscription

    device = factory.SubFactory(DeviceFactory)
    post = factory.SubFactory(PostFactory)
