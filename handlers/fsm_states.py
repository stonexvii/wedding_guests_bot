from aiogram.fsm.state import State, StatesGroup


class ShowAnswer(StatesGroup):
    next_answer = State()
