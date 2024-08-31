from aiogram import Router, F
from aiogram.types import CallbackQuery
from modules.english_words.keyboards import fabrics, inline
from modules.english_words.keyboards.inline import trans_kb
from modules.english_words.utils.states import Form
from modules.english_words.callbacks.topics import topic_from_table, words_from_theme
from modules.english_words.keyboards.fabrics import create_paginator, create_theme_paginator
from aiogram.fsm.context import FSMContext

router = Router()

"""
This file defines a set of callback query handlers for a Telegram bot built using the aiogram library.
Each handler is responsible for processing a specific callback data value and sending an appropriate response 
to the user.

Here's a brief overview of the handlers:

1. send_info_devs: Displays information about the developers of the bot when the user clicks on a "devs" button.
2. send_bot_info: Provides information about the bot's purpose when the user clicks on a "bot_info" button.
3. button_back: Returns the user to the main menu or a greeting message when the user clicks on a "back" button.
4. topics: Allows the user to choose a section for learning words when the "topics" button is clicked.
5. support: Prompts the user to choose a translation language when the "translate_api" button is clicked.
6. ukr_trans: Sets the bot's state to expect an English word from the user for translation into Ukrainian.
7. eng_trans: Sets the bot's state to expect a word in another language (such as Ukrainian) for translation into English.
8. topic: Handles the selection of a topic by the user and displays available themes related to that topic.
9. theme: Displays a list of words or themes within a selected subject or category.
10. words: Retrieves and displays the definition or translation of a word based on the selected theme or category.

These handlers are part of the bot's dialogue management system, providing users with an interactive 
and structured way to learn English words and phrases.
"""


@router.callback_query(F.data == "devs")
async def send_info_devs(callback: CallbackQuery):
    await callback.message.edit_text('Хей 🎭 ось розробники цього бота)\n\nПриємного користування! ☺️',
                                     reply_markup=inline.linsk_kb)


@router.callback_query(F.data == "bot_info")
async def send_bot_info(callback: CallbackQuery):
    await callback.message.edit_text(
        'Цей бот створенний для вивчення нових англійських слів по різним рівням, окремим темам чи по тестам, такі як: IELTS',
        reply_markup=inline.back_kb)


@router.callback_query(F.data == "back")
async def button_back(callback: CallbackQuery):
    await callback.message.edit_text(
        f'Давай вивчати англійську разом 🇬🇧\n\n'
        f'Ти можеш обрати розділ з необхідними темами, або вивчати нові слова на своєму рівні\n\n\n'
        f'Keep going! \n\n'
        f'⬇️Обери необхідний пункт нижче⬇️\n',
        reply_markup=fabrics.greeting())


@router.callback_query(F.data == "topics")
async def topics(callback: CallbackQuery):
    await callback.message.edit_text('Супер!🥳 \n\nДавай оберемо розділ для вивчення слів💫',
                                     reply_markup=inline.topics_kb)


@router.callback_query(F.data == "translate_api")
async def support(callback: CallbackQuery) -> None:
    await callback.message.edit_text('Оберіть мову перекладу :)', reply_markup=trans_kb)


@router.callback_query(F.data == "ukraine")
async def ukr_trans(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.word)
    await callback.message.edit_text(
        'Напишіть слово для перекладу ')


@router.callback_query(F.data == "english")
async def eng_trans(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.slovo)
    await callback.message.edit_text(
        'Напишіть слово для перекладу ')


@router.callback_query(F.data.startswith('topic:'))
async def topic(callback: CallbackQuery, state: FSMContext):
    button_info = callback.data.split(':')
    table = button_info[1].split('_')
    my_paginator = await create_theme_paginator(' '.join(table), ' ', 'topic')
    await callback.message.edit_text("Оберіть тему:", reply_markup=my_paginator(0))


@router.callback_query(F.data.startswith('theme:'))
async def theme(callback: CallbackQuery):
    button_info = callback.data.split(':')
    group_subject = button_info[2].split('_')
    table = button_info[1].split('_')
    my_paginator = await create_theme_paginator(' '.join(table), ' '.join(group_subject), 'theme')
    await callback.message.edit_text("Оберіть тему:", reply_markup=my_paginator(0))


@router.callback_query(F.data.startswith('words:'))
async def words(callback: CallbackQuery):
    button_info = callback.data.split(':')
    table = button_info[1].split("_")
    theme = button_info[2].split("_")
    word_definition = await words_from_theme(' '.join(table), ' '.join(theme))
    my_paginator = await create_paginator(button_info[1], button_info[2])
    print(word_definition)
    await callback.message.edit_text(f'{word_definition[0]}', reply_markup=my_paginator())


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery) -> None:
    await callback.message.edit_text('Ваш профіль', reply_markup=inline.profile_kb)