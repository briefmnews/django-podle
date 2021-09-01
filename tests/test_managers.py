import pytest

from podle.models import Newsletter, RssFeed
from podle.podle import PodleHelper
from .factories import DummyDataFactory

pytestmark = pytest.mark.django_db()


class TestNewsletterManager:
    def test_create_newsletter(self, mock_create_newsletter):
        # GIVEN
        dummy_instance = DummyDataFactory()

        # WHEN
        newsletter = Newsletter.objects.create_or_update_newsletter(dummy_instance, {})

        # THEN
        assert newsletter
        mock_create_newsletter.assert_called_once_with({})

    def test_update_newsletter(self, mock_create_newsletter, newsletter):
        # GIVEN
        dummy_instance = DummyDataFactory(id=newsletter.object_id)

        # WHEN
        response = Newsletter.objects.create_or_update_newsletter(dummy_instance, {})

        # THEN
        assert response
        mock_create_newsletter.assert_called_once_with(
            {"newsletterId": str(newsletter.uuid)}
        )


class TestRssFeedManager:
    def test_get_rss_feed_with_existing_feed(self, rss_feed):
        # WHEN
        response = RssFeed.objects.get_rss_feed(rss_feed.user)

        # THEN
        assert response == rss_feed.feed

    def test_get_rss_feed_without_feed(self, user):
        # WHEN
        response = RssFeed.objects.get_rss_feed(user)

        # THEN
        assert not response

    def test_create_rss_feed(self, users, mocker, settings):
        # GIVEN
        mock_create_batch_private_rss = mocker.patch.object(
            PodleHelper,
            "create_batch_private_rss",
            return_value=[{user.pk: "https://dummyurl.io"} for user in users],
        )
        assert RssFeed.objects.count() == 0

        # WHEN
        RssFeed.objects.create_rss_feed(users)

        # THEN
        assert RssFeed.objects.count() == users.count()
        mock_create_batch_private_rss.assert_called_once_with(
            {
                "subscribers": [
                    {
                        "subscriberId": user.pk,
                        "newsletterName": settings.PODLE_NEWSLETTER_NAME,
                    }
                    for user in users
                ]
            }
        )

    def test_delete_rss_feed(self, users_with_rss_feeds, mocker, settings):
        # GIVEN
        mock_delete_batch_private_rss = mocker.patch.object(
            PodleHelper,
            "delete_batch_private_rss",
            return_value=[{user.pk: "deleted"} for user in users_with_rss_feeds],
        )
        assert RssFeed.objects.count() == users_with_rss_feeds.count()

        # WHEN
        RssFeed.objects.delete_rss_feed(users_with_rss_feeds)

        # THEN
        assert RssFeed.objects.count() == 0
        mock_delete_batch_private_rss.assert_called_once_with(
            {
                "subscribers": [
                    {
                        "subscriberId": user.pk,
                        "newsletterName": settings.PODLE_NEWSLETTER_NAME,
                    }
                    for user in users_with_rss_feeds
                ]
            }
        )
