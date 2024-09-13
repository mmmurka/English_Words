from aiogram.fsm.state import State, StatesGroup


class WordState(StatesGroup):
    """
    The Form class defines a set of states for a finite state machine (FSM) used in the aiogram library.
    FSM allows you to manage user dialogues by transitioning between different states.
    In this case, we have two states:
    1. eng_word - a state where the bot expects the input of an English word.
    2. ukr_word - a state where the bot expects the input of a word in another language, such as Russian.
    Using FSM helps organize the logic of user interactions, allowing the bot to track which stage of the dialogue
    the user is in and what actions should be performed next.
    """

    eng_word = State()
    ukr_word = State()


class PaginationWord(StatesGroup):
    words = State()
    definition = State()
