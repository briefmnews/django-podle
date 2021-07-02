import pytest

from .factories import DictionaryFactory, RssFeedFactory
from podle.models import Dictionary

pytestmark = pytest.mark.django_db()


class TestDictionaryHandlers:
    def test_create_dictionary_word(self, mock_create_or_update_word):
        # GIVEN
        assert not Dictionary.objects.filter(word="hello").exists()

        # WHEN
        DictionaryFactory(pronunciation="hello", word="hello")

        # THEN
        mock_create_or_update_word.assert_called_once_with(
            {"value": "hello", "raw": "hello"}
        )

    def test_update_dictionary_word(self, word, mock_create_or_update_word):
        # WHEN
        word.pronunciation = "change"
        word.save()

        # THEN
        mock_create_or_update_word.assert_called_once_with(
            {"value": word.pronunciation, "raw": word.word}
        )

    def test_create_dictionary_word_with_error_in_response(
        self, mock_create_or_update_word
    ):
        # GIVEN
        mock_create_or_update_word.return_value = {}

        # WHEN / THEN
        with pytest.raises(Exception):
            DictionaryFactory(pronunciation="hello", word="hello")

    def test_delete_dictionary_word(self, word, mock_delete_word):
        # WHEN
        word.delete()

        # THEN
        mock_delete_word.assert_called_once_with(word.word)

    def test_delete_dictionary_word_with_error_in_response(
        self, word, mock_delete_word
    ):
        # GIVEN
        mock_delete_word.return_value = {}

        # WHEN / THEN
        with pytest.raises(Exception):
            word.delete()


class TestRssFeedHandlers:
    def test_create_rss_feed(self, mock_create_private_rss, user, settings):
        # GIVEN
        mock_create_private_rss.return_value = {str(user.pk): "http://www.example.rss"}
        # WHEN
        RssFeedFactory(user=user, feed="")

        # THEN
        mock_create_private_rss.assert_called_once_with(
            {
                "subscriberId": user.pk,
                "newsletterName": settings.PODLE_NEWSLETTER_NAME,
            }
        )

    def test_create_rss_feed_with_error_in_response(
        self, mock_create_private_rss, user
    ):
        # GIVEN
        mock_create_private_rss.return_value = {str(user.pk): ""}
        # WHEN / THEN
        with pytest.raises(Exception):
            RssFeedFactory(user=user, feed="")

    def test_delete_rss_feed(self, mock_delete_private_rss, rss_feed, settings):
        # GIVEN
        mock_delete_private_rss.return_value = {str(rss_feed.user.pk): "deleted"}

        # WHEN
        rss_feed.delete()

        # THEN
        mock_delete_private_rss.assert_called_once_with(
            rss_feed.user.pk, settings.PODLE_NEWSLETTER_NAME
        )

    def test_delete_rss_feed_with_error_in_response(
        self, mock_delete_private_rss, rss_feed
    ):
        # GIVEN
        mock_delete_private_rss.return_value = {str(rss_feed.user.pk): ""}

        # WHEN / THEN
        with pytest.raises(Exception):
            rss_feed.delete()
