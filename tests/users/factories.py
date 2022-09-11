import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from faker import Faker

fake = Faker()


def generate_random_ewkt():
    latitude, longitude = fake.latlng()
    return f"SRID=4326;POINT ({longitude} {latitude})"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)

    email = factory.Faker("email")
    password = factory.Faker("password")
    nickname = factory.Faker("first_name")
    is_active = factory.Faker("pybool")
    is_admin = False
    address = factory.Faker("address")
    auth_provider = FuzzyChoice([None, "APPLE", "KAKAO"])
    location = factory.LazyFunction(generate_random_ewkt)
