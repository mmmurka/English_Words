from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from modules.words.utils.states import WordState
from modules.words.keyboards.inline import translate_kb as tr
from modules.words.keyboards.inline import translate as tran

from layers.translate_api.translateAPI import trans_text


router = Router()


@router.message(WordState.eng_word)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(word=message.text)
    data: dict = await state.get_data()
    await state.clear()

    word: str = data.get("word")

    translation_result = await trans_text(text=word, src="en", dest="uk")

    await message.answer(translation_result, reply_markup=tr)


@router.message(WordState.ukr_word)
async def form_slovo(message: Message, state: FSMContext) -> None:
    await state.update_data(slovo=message.text)
    data: dict = await state.get_data()
    await state.clear()

    slovo: str = data.get("slovo")

    translation_result = await trans_text(text=slovo, src="uk", dest="en")

    await message.answer(translation_result, reply_markup=tran)
