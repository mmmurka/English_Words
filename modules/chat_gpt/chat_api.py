import os

import openai
from openai import AsyncOpenAI


class ChatGPT:
    def __init__(self, role: str = "You are an English teacher assisting users in learning English,"
                                   " answering their questions, correcting their mistakes,"
                                   " and providing encouragement and additional learning resources,"
                                   " my native language is English."):
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key
        self.role = role
        self.client = AsyncOpenAI()

    async def get_response(self, user_message: str) -> str:
        # Создание запроса к OpenAI API
        completion = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.role},
                {"role": "user", "content": user_message}
            ]
        )

        # Получаем ответ от ChatGPT
        gpt_reply = completion.choices[0].message.content
        return gpt_reply
