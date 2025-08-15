from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.tables import QuestionsTable, AnswersTable
from .callback_data import UserAnswer, ShowAnswer


def ikb_answers(user_id: int, quest_data: list[QuestionsTable, list[AnswersTable]]):
    keyboard = InlineKeyboardBuilder()
    question, answers = quest_data
    for answer in answers:
        keyboard.button(
            text=answer.answer,
            callback_data=UserAnswer(
                user_id=user_id,
                question_id=question.id,
                answer_id=answer.answer_id,
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_show_answer(answers: list[tuple[int, int]], answers_text: dict[int, str]):
    keyboard = InlineKeyboardBuilder()
    if answers:
        for answer_id, answer_amount in answers:
            keyboard.button(
                text=answers_text[answer_id],
                callback_data=ShowAnswer(
                    button='target',
                    target_answer=answer_id,
                    answer_amount=answer_amount,
                ),
            )
    else:
        keyboard.button(
            text='Очистить',
            callback_data=ShowAnswer(
                button='reset',
                target_answer=0,
                answer_amount=0,
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()
