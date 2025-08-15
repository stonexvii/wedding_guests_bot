from aiogram.filters.callback_data import CallbackData


class UserAnswer(CallbackData, prefix='UA'):
    user_id: int
    question_id: int
    answer_id: int


class ShowAnswer(CallbackData, prefix='SA'):
    button: str
    target_answer: int
    answer_amount: int


class CurrentQuestion(CallbackData, prefix='CQ'):
    button: str
    question_id: int


class QuestionNavigate(CallbackData, prefix='QN'):
    button: str
    question_id: int = 0
