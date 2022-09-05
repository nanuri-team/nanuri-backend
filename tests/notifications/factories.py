import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from faker import Faker

from nanuri.notifications.models import Device, Subscription

from ..users.factories import UserFactory

fake = Faker()


def generate_random_ewkt():
    latitude, longitude = fake.latlng()
    return f"SRID=4326;POINT ({longitude} {latitude})"


class DeviceFactory(DjangoModelFactory):
    class Meta:
        model = Device

    user = factory.SubFactory(UserFactory)
    device_token = factory.Faker("sha256")
    opt_in = factory.Faker("pybool")
    location = factory.Faker("pystr_format", string_format=generate_random_ewkt())


class SubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = Subscription

    device = factory.SubFactory(DeviceFactory)
    topic = FuzzyChoice(Subscription.Topic.values)
    group_code = factory.Faker("uuid4")
    opt_in = factory.Faker("pybool")
