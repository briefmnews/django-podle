import pytest

from podle.models import Newsletter
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
