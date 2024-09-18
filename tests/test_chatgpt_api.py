import pytest
from unittest.mock import AsyncMock, patch
from modules.chat_gpt.chat_api import ChatGPT


@pytest.mark.asyncio
@patch('modules.chat_gpt.chat_api.AsyncOpenAI')
async def test_get_response(mock_openai_client):
    mock_completion = AsyncMock()
    mock_completion.choices = [AsyncMock(message=AsyncMock(content="Random response"))]

    mock_openai_client().chat.completions.create = AsyncMock(return_value=mock_completion)

    chat_gpt = ChatGPT()

    response = await chat_gpt.get_response("What is the capital of France?")

    assert response is not None
    assert isinstance(response, str)

    mock_openai_client().chat.completions.create.assert_awaited_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": chat_gpt.role},
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
