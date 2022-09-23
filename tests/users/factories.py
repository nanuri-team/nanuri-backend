import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from faker import Faker

from nanuri.users.models import User

fake = Faker()


def generate_random_ewkt():
    latitude, longitude = fake.latlng()
    return f"SRID=4326;POINT ({longitude} {latitude})"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

    email = factory.Faker("email")
    password = factory.Faker("password")
    nickname = factory.Faker("first_name")
    is_active = factory.Faker("pybool")
    is_admin = False
    auth_provider = FuzzyChoice([None, "APPLE", "KAKAO"])
    location = factory.LazyFunction(generate_random_ewkt)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        instance = super()._create(model_class, *args, **kwargs)
        instance.set_password(instance.password)
        instance.save()
        return instance
