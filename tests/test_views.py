import json
import pytest

from podle.views import NewsletterWebhook

pytestmark = pytest.mark.django_db()


class TestNewsletterWebhook:
    def test_post_works(self, newsletter, request_builder):
        # GIVEN
        assert not newsletter.audio_url
        filename = "tests/fixtures/webhook.json"
        with open(filename) as f:
            webhook_response = json.load(f)

        request = request_builder.post(data=webhook_response)

        # WHEN
        response = NewsletterWebhook.as_view()(request)

        # THEN
        assert response.status_code == 200
        newsletter.refresh_from_db()
        assert newsletter.audio_url == webhook_response["newsletter_url"]

    def test_post_404(self, request_builder):
        # GIVEN
        filename = "tests/fixtures/webhook.json"
        with open(filename) as f:
            webhook_response = json.load(f)

        request = request_builder.post(data=webhook_response)

        # WHEN
        response = NewsletterWebhook.as_view()(request)

        # THEN
        assert response.status_code == 404
