import pytest
from unittest.mock import AsyncMock, patch
from modules.chat_gpt.chat_api import ChatGPT


@pytest.mark.asyncio
@patch('modules.chat_gpt.chat_api.AsyncOpenAI')
async def test_get_response(mock_openai_client):
    mock_completion = AsyncMock()
    mock_completion.choices = [AsyncMock(message=AsyncMock(content="Random response"))]

    mock_openai_client().chat.completions.create = AsyncMock(return_value=mock_completion)

    chat_gpt = ChatGPT(role="You are an English teacher assisting users in learning English,"
                                   " answering their questions, correcting their mistakes,"
                                   " and providing encouragement and additional learning resources,"
                                   " my native language is ukrainian,"
                                   "and use emojis.")

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


@pytest.mark.asyncio
@patch('modules.chat_gpt.chat_api.AsyncOpenAI')
@patch('modules.chat_gpt.chat_api.logging')
async def test_get_response_exception_handling(mock_logging, mock_openai_client):
    exception_message = "OpenAI error"
    mock_openai_client().chat.completions.create = AsyncMock(side_effect=Exception(exception_message))

    chat_gpt = ChatGPT(role="You are an English teacher assisting users in learning English,"
                             " answering their questions, correcting their mistakes,"
                             " and providing encouragement and additional learning resources,"
                             " my native language is ukrainian,"
                             "and use emojis.")

    response = await chat_gpt.get_response("What is the capital of France?")

    assert response is None

    mock_logging.error.assert_called_once()
    logged_exception = mock_logging.error.call_args[0][0]
    assert isinstance(logged_exception, Exception)
    assert str(logged_exception) == exception_message

    mock_openai_client().chat.completions.create.assert_awaited_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": chat_gpt.role},
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
