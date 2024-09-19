import logging
import os

import openai
from openai import AsyncOpenAI


class ChatGPT:
    def __init__(self, role: str):
        self.api_key: str = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key
        self.role: str = role
        self.client: AsyncOpenAI = AsyncOpenAI()

    async def get_response(self, user_message: str) -> str:
        try:
            completion = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.role},
                    {"role": "user", "content": user_message}
                ]
            )

            gpt_reply = completion.choices[0].message.content
            return gpt_reply
        except Exception as e:
            logging.error(e)
