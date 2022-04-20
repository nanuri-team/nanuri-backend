import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("email")
    password = factory.Faker("password")
    nickname = factory.Faker("first_name")
    is_active = factory.Faker("pybool")
    is_admin = False
    latitude = factory.Faker("pyfloat", min_value=-90, max_value=90)
    longitude = factory.Faker("pyfloat", min_value=-90, max_value=90)
    address = factory.Faker("address")
    profile_url = factory.Faker("image_url")
    auth_provider = FuzzyChoice([None, "APPLE", "KAKAO"])
