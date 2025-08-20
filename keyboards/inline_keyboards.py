from aiogram.utils.keyboard import InlineKeyboardBuilder

from collections import namedtuple

from database.tables import QuestionsTable, AnswersTable
from .callback_data import UserAnswer, ShowAnswer, CurrentQuestion, QuestionNavigate

Button = namedtuple('Button', ['text', 'callback'])


def ikb_questions(questions: list[QuestionsTable]):
    keyboard = InlineKeyboardBuilder()
    for question in sorted(questions, key=lambda x: x.id):
        keyboard.button(
            text=f'{question.id}: {question.question}',
            callback_data=CurrentQuestion(
                button='target',
                question_id=question.id,
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_question_menu(question_id: int):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Отправить', 'send'),
        Button('Сколько?', 'amount'),
        Button('Результаты', 'results'),
        Button('Удалить', 'delete'),
        Button('Сбросить', 'reset'),
        Button('Назад', 'back'),
    ]
    for button in buttons:
        keyboard.button(
            text=button.text,
            callback_data=QuestionNavigate(
                button=button.callback,
                question_id=question_id,
            ),
        )
    keyboard.adjust(3, 2)
    return keyboard.as_markup()


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


def ikb_show_answer(answers: list[tuple[int, int, int]], answers_text: dict[int, str]):
    keyboard = InlineKeyboardBuilder()
    if answers:
        for position, answer_id, answer_amount in answers:
            keyboard.button(
                text=answers_text[answer_id],
                callback_data=ShowAnswer(
                    button='target',
                    position=position,
                    target_answer=answer_id,
                    answer_amount=answer_amount,
                ),
            )
    else:
        keyboard.button(
            text='Очистить',
            callback_data=ShowAnswer(
                button='reset',
                position=0,
                target_answer=0,
                answer_amount=0,
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()
