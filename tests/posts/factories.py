from datetime import timedelta

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from nanuri.posts.models import Category, Post, PostImage

from ..users.factories import UserFactory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.Faker("safe_color_name")
    parent = None


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence")
    image = factory.Faker("image_url")
    unit_price = factory.Faker("pyint", min_value=10000, max_value=200000, step=100)
    quantity = factory.Faker("pyint", min_value=1, max_value=30)
    description = factory.Faker("paragraph")
    min_participants = factory.Faker("pyint", min_value=3, max_value=8)
    max_participants = factory.Faker("pyint", min_value=10, max_value=20)
    num_participants = factory.Faker("pyint", min_value=0, max_value=7)
    product_url = factory.Faker("uri")
    trade_type = FuzzyChoice(choices=["DIRECT", "PARCEL"])
    order_status = "WAITING"
    is_published = True
    published_at = factory.Faker(
        "date_time_this_month", tzinfo=timezone.get_current_timezone()
    )
    view_count = factory.Faker("pyint")
    waited_from = factory.LazyAttribute(lambda x: x.published_at.date())
    waited_until = factory.LazyAttribute(lambda x: x.waited_from + timedelta(days=3))

    writer = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)


class PostImageFactory(DjangoModelFactory):
    class Meta:
        model = PostImage

    post = factory.SubFactory(PostFactory)
    image = factory.Faker("image_url")
