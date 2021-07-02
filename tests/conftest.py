import pytest

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory

from podle.managers import PodleHelper
from .factories import NewsletterFactory, DictionaryFactory, RssFeedFactory, UserFactory


@pytest.fixture
def newsletter():
    return NewsletterFactory()


@pytest.fixture
def word(mock_create_or_update_word):
    word = DictionaryFactory()
    mock_create_or_update_word.reset_mock()
    return word


@pytest.fixture
def rss_feed():
    return RssFeedFactory()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def mock_create_newsletter(mocker):
    return mocker.patch.object(
        PodleHelper,
        "create_newsletter",
        return_value={"id": "54d880a5-9b4f-4253-8ce7-e467ec85dfb2"},
    )


@pytest.fixture
def mock_create_or_update_word(mocker):
    return mocker.patch.object(
        PodleHelper,
        "create_or_update_word",
        return_value={"added": {"hello": "hello"}},
    )


@pytest.fixture
def mock_delete_word(mocker):
    return mocker.patch.object(
        PodleHelper,
        "delete_word",
        return_value={"deleted": "hello"},
    )


@pytest.fixture
def mock_create_private_rss(mocker):
    return mocker.patch.object(
        PodleHelper,
        "create_private_rss",
    )


@pytest.fixture
def mock_delete_private_rss(mocker):
    return mocker.patch.object(
        PodleHelper,
        "delete_private_rss",
    )


@pytest.fixture
def request_builder():
    return RequestBuilder()


class RequestBuilder:
    @staticmethod
    def post(
        path="/",
        user=None,
        data=None,
    ):
        rf = RequestFactory()
        request = rf.post(path=path, data=data)
        request.user = user or AnonymousUser()

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        return request
