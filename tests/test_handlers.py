import pytest

from .factories import DictionaryFactory
from podle.models import Dictionary

pytestmark = pytest.mark.django_db()


class TestHandlers:
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

    def test_delete_dictionary_word(self, word, mock_delete_word):
        # WHEN
        word.delete()

        # THEN
        mock_delete_word.assert_called_once_with(word.word)
