import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from nanuri.notifications.models import Device, Subscription

from ..users.factories import UserFactory


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
    topic = FuzzyChoice(
        choices=[
            "TO_ALL",
            "TO_POST_WRITER",
            "TO_POST_PARTICIPANTS",
            "TO_CHAT_ROOM",
        ],
    )
    group_code = factory.Faker("uuid4")
    opt_in = factory.Faker("pybool")
