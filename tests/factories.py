import factory
import uuid

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from podle.models import Newsletter, Dictionary, RssFeed
from .models import DummyData

User = get_user_model()


class DummyDataFactory(factory.django.DjangoModelFactory):
    data = factory.Sequence(lambda n: f"content {n}")

    class Meta:
        model = DummyData


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class NewsletterFactory(factory.django.DjangoModelFactory):
    uuid = uuid.UUID("54d880a5-9b4f-4253-8ce7-e467ec85dfb2")
    audio_url = ""
    content_type = factory.LazyAttribute(
        lambda _: ContentType.objects.get_for_model(DummyData)
    )
    object_id = factory.Sequence(int)

    class Meta:
        model = Newsletter


class DictionaryFactory(factory.django.DjangoModelFactory):
    word = factory.sequence(lambda n: f"word {n}")
    pronunciation = factory.sequence(lambda n: f"pronunciation {n}")

    class Meta:
        model = Dictionary


class RssFeedFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    feed = factory.sequence(lambda n: f"http://example.com/{n}.rss")

    class Meta:
        model = RssFeed
