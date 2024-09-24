import pytest
from unittest.mock import patch, MagicMock
from layers.translate_api.translateAPI import trans_text


@pytest.mark.asyncio
async def test_trans_text_en_to_uk():
    with patch('layers.translate_api.translateAPI.Translator') as MockTranslator:
        mock_translator_instance = MockTranslator.return_value

        mock_translation_uk = MagicMock()
        mock_translation_uk.text = "гра не коштує свічок"  # expected translation result
        mock_translator_instance.translate.return_value = mock_translation_uk

        # Call the testable function for translation from English to Ukrainian
        result_uk = await trans_text(text="the game is not worth the candle", src='en', dest='uk')

        # Checking the result
        assert result_uk == "гра не коштує свічок"
        mock_translator_instance.translate.assert_called_once_with(text="the game is not worth the candle",
                                                                   src='en', dest='uk')


@pytest.mark.asyncio
async def test_trans_text_uk_to_en():
    with patch('layers.translate_api.translateAPI.Translator') as MockTranslator:
        mock_translator_instance = MockTranslator.return_value

        mock_translation_en = MagicMock()
        mock_translation_en.text = "love while the body is young, because in old age only the eyes will love"
        mock_translator_instance.translate.return_value = mock_translation_en

        result_en = await trans_text(text="люби, поки тіло молоде, бо в старості будуть любити тільки очі",
                                     src='uk', dest='en')

        assert result_en == "love while the body is young, because in old age only the eyes will love"
        mock_translator_instance.translate.assert_called_once_with(
            text="люби, поки тіло молоде, бо в старості будуть любити тільки очі", src='uk', dest='en')


@pytest.mark.asyncio
async def test_trans_text_failure():
    with patch('layers.translate_api.translateAPI.Translator') as MockTranslator:
        mock_translator_instance = MockTranslator.return_value
        mock_translator_instance.translate.side_effect = Exception("Translation Error")

        result = await trans_text(text="text", src='en', dest='uk')

        assert isinstance(result, Exception)
        assert str(result) == "Translation Error"


@pytest.mark.asyncio
async def test_trans_text_empty_text():
    with patch('layers.translate_api.translateAPI.Translator') as MockTranslator:
        mock_translator_instance = MockTranslator.return_value

        mock_translation = MagicMock()
        mock_translation.text = ""

        mock_translator_instance.translate.return_value = mock_translation

        result = await trans_text(text="", src='en', dest='uk')

        assert result == ""

        mock_translator_instance.translate.assert_called_once_with(
            text="", src='en', dest='uk'
        )

#aaaaa
