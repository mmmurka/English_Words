from googletrans import Translator
import logging


async def trans_text(text='text', src='en', dest='uk') -> str | Exception:
    try:
        translator = Translator()
        translation = translator.translate(text=text, src=src, dest=dest)

        return translation.text
    except Exception as ex:
        logging.error(f'Error in translation {ex}')
        return ex
