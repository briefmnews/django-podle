import pytest

from .factories import DictionaryFactory, RssFeedFactory
from podle.models import Dictionary, RssFeed
from podle.signals.handlers import handle_rss_feeds

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

    def test_handle_rss_feeds_with_single_user_post_add(
        self, group_rss_feed, user, mock_create_private_rss
    ):
        # GIVEN
        mock_create_private_rss.return_value = {str(user.pk): "http://www.example.rss"}
        group_pks = [group_rss_feed.pk]
        group_rss_feed.user_set.add(user)

        # WHEN
        handle_rss_feeds(
            instance=user,
            action="post_add",
            reverse=False,
            model=RssFeed,
            pk_set=set(group_pks),
            using="default",
        )

        # THEN
        assert mock_create_private_rss.call_count == 1

    def test_handle_rss_feeds_with_single_user_post_remove(
        self, rss_feed, group_rss_feed, mock_delete_private_rss
    ):
        # GIVEN
        user = rss_feed.user
        mock_delete_private_rss.return_value = {str(user.pk): "deleted"}
        group_pks = [group_rss_feed.pk]
        group_rss_feed.user_set.add(user)

        # WHEN
        handle_rss_feeds(
            instance=user,
            action="post_remove",
            reverse=False,
            model=RssFeed,
            pk_set=set(group_pks),
            using="default",
        )

        # THEN
        assert mock_delete_private_rss.call_count == 1

    def test_handle_rss_feed_works_with_reverse_m2m_post_add(
        self, group_rss_feed, user, mock_create_private_rss
    ):
        # GIVEN
        mock_create_private_rss.return_value = {str(user.pk): "http://www.example.rss"}

        # WHEN
        handle_rss_feeds(
            instance=group_rss_feed,
            action="post_add",
            reverse=True,
            model=RssFeed,
            pk_set=[user.pk],
            using="default",
        )

        # THEN
        assert mock_create_private_rss.call_count == 1

    def test_handle_rss_feed_works_with_reverse_m2m_post_remove(
        self, group_rss_feed, mock_delete_private_rss, rss_feed
    ):
        # GIVEN
        user = rss_feed.user
        mock_delete_private_rss.return_value = {str(user.pk): "deleted"}

        # WHEN
        handle_rss_feeds(
            instance=group_rss_feed,
            action="post_remove",
            reverse=True,
            model=RssFeed,
            pk_set=[user.pk],
            using="default",
        )

        # THEN
        assert mock_delete_private_rss.call_count == 1

    @pytest.mark.parametrize("action", ["post_add", "post_remove"])
    def test_handle_rss_feed_with_group_not_in_pk_set(self, action, user):
        # GIVEN / WHEN
        response = handle_rss_feeds(
            instance=user,
            action=action,
            reverse=False,
            model=RssFeed,
            pk_set={0},
            using="default",
        )

        # THEN
        assert not response
