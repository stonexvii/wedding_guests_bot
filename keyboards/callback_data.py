from aiogram.filters.callback_data import CallbackData


class UserAnswer(CallbackData, prefix='UA'):
    user_id: int
    question_id: int
    answer_id: int


class ShowAnswer(CallbackData, prefix='SA'):
    button: str
    target_answer: int
    answer_amount: int
