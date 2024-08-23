from googletrans import Translator


async def trans_text(text='text', src='en', dest='uk'):
    try:
        translator = Translator()
        translation = translator.translate(text=text, src=src, dest=dest)

        return translation.text
    except Exception as ex:
        return ex
