from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from Telegram.utils.states import Form
from Telegram.keyboards.builders import profile
from Telegram.keyboards.inline import translate_kb as tr

from Telegram.translate.translateAPI import trans_text


router = Router()


@router.message(Form.word)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(word=message.text)
    data = await state.get_data()
    await state.clear()

    word = data.get('word')

    translation_result = await trans_text(text=word, src='en', dest='uk')

    await message.answer(translation_result, reply_markup=tr)















