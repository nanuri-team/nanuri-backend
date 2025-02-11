from datetime import timedelta

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from nanuri.posts.models import Comment, Post, PostImage, SubComment

from ..users.factories import UserFactory


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
    category = FuzzyChoice(
        choices=["BATHROOM", "FOOD", "KITCHEN", "HOUSEHOLD", "STATIONERY", "ETC"]
    )


class PostImageFactory(DjangoModelFactory):
    class Meta:
        model = PostImage

    post = factory.SubFactory(PostFactory)
    image = factory.Faker("image_url")


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    text = factory.Faker("sentence")
    writer = factory.SubFactory(UserFactory)


class SubCommentFactory(DjangoModelFactory):
    class Meta:
        model = SubComment

    comment = factory.SubFactory(CommentFactory)
    text = factory.Faker("sentence")
    writer = factory.SubFactory(UserFactory)
