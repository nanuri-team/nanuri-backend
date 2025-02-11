import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from faker import Faker

from nanuri.notifications.models import Device, Subscription

from ..users.factories import UserFactory

fake = Faker()


class DeviceFactory(DjangoModelFactory):
    class Meta:
        model = Device

    user = factory.SubFactory(UserFactory)
    device_token = factory.Faker("sha256")
    opt_in = factory.Faker("pybool")


class SubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = Subscription

    device = factory.SubFactory(DeviceFactory)
    topic = FuzzyChoice(Subscription.Topic.values)
    group_code = factory.Faker("uuid4")
    opt_in = factory.Faker("pybool")
