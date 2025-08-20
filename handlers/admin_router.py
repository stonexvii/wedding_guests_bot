from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

import os

import config
from classes import FileManager, push_message
from database import requests
from .fsm_states import ShowAnswer
from keyboards import ikb_questions, ikb_answers, ikb_show_answer, ikb_question_menu
from keyboards.callback_data import CurrentQuestion, QuestionNavigate
from middlewares import AdminMiddleware
from misc import build_text_message

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.callback_query(QuestionNavigate.filter(F.button == 'back'))
@admin_router.message(Command('begin'))
async def start_wedding(message: Message | CallbackQuery, bot: Bot):
    questions = await requests.all_questions()
    if isinstance(message, Message):
        await message.answer(
            text='Выбери вопрос:',
            reply_markup=ikb_questions(questions),
        )
    else:
        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=message.message.message_id,
            text='Выбери вопрос:',
            reply_markup=ikb_questions(questions),
        )


@admin_router.callback_query(CurrentQuestion.filter(F.button == 'target'))
async def target_question(callback: CallbackQuery, callback_data: CurrentQuestion, bot: Bot):
    question_id = callback_data.question_id
    question = await requests.get_question(question_id)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=build_text_message(question),
        reply_markup=ikb_question_menu(question_id),
    )


@admin_router.message(Command('write'))
async def command_write(message: Message, command: CommandObject):
    file_name, data = command.args.split(' ', 1)
    await FileManager.write(file_name, data)
    await message.answer(
        text=data,
    )


@admin_router.message(Command('del'))
async def command_del(message: Message, command: CommandObject):
    if command.args:
        print('YES')
        file_names = command.args.split()
        for file_name in file_names:
            file_path = os.path.join('messages', f'{file_name}.txt')
            if os.path.exists(file_path):
                os.remove(os.path.join('messages', f'{file_name}.txt'))
    else:
        files = os.listdir('messages')
        for file in files:
            if file.endswith('.txt') and file.split('.')[0] not in ('intro', 'cap'):
                os.remove(os.path.join('messages', file))


@admin_router.message(Command('set'))
async def command_set(message: Message, command: CommandObject):
    question_id, question_data = command.args.split(' ', 1)
    question, *answers = question_data.split('\n')
    await requests.set_question(
        question_id=int(question_id),
        question_text=question,
        answers=answers,
    )


@admin_router.callback_query(QuestionNavigate.filter(F.button == 'delete'))
async def question_delete(callback: CallbackQuery, callback_data: QuestionNavigate, bot: Bot):
    question_id = callback_data.question_id
    await requests.delete_question(
        question_id=question_id,
    )
    await callback.answer(
        text=f'Вопрос #{question_id} удален!',
        show_alert=True,
    )
    await start_wedding(callback, bot)


@admin_router.callback_query(QuestionNavigate.filter(F.button == 'results'))
async def question_results(callback: CallbackQuery, callback_data: QuestionNavigate, state: FSMContext, bot: Bot):
    await state.set_state(ShowAnswer.next_answer)
    question_id = callback_data.question_id
    quest_data = await requests.get_question(question_id)
    question, answers = quest_data
    json_data = {
        'question': question.question,
        'answer_1': '',
        'answer_2': '',
        'answer_3': '',
        'answer_4': '',
    }
    if os.path.exists(os.path.join('messages', f'{question_id}.txt')):
        data = await FileManager.read(str(question_id))
        answers_count = {idx: count for idx, count in enumerate(map(int, data.strip().split()), 1)}
    else:
        user_answers = await requests.collect_answers(question_id)
        answers_count = {ans.answer_id: user_answers.count(ans.answer_id) for ans in answers}
    answers_dict = {answer.answer_id: answer.answer for answer in answers}
    answers_list = [(pos, answer_id, answer_amount) for pos, (answer_id, answer_amount) in
                    enumerate(sorted(list(answers_count.items()), key=lambda x: x[1], reverse=True), 1)]
    msg_txt = f'{question.question}\n'
    if answers:
        for answer in answers:
            count = answers_count[answer.answer_id]
            msg_txt += f'\t{count} {answer.answer}\n'
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=msg_txt,
        reply_markup=ikb_show_answer(answers_list, answers_dict),
    )
    push_message(json_data)
    await state.set_data({
        'json': json_data,
        'answers_list': answers_list,
        'answers_dict': answers_dict,
        'text': msg_txt,
        'question': question.question,
    })


@admin_router.callback_query(QuestionNavigate.filter(F.button == 'reset'))
async def reset_user_answers(callback: CallbackQuery, callback_data: QuestionNavigate):
    await requests.delete_answers(callback_data.question_id)
    await callback.answer(
        text=f'Ответы пользователей для вопроса #{callback_data.question_id} удалены!',
        show_alert=True,
    )


@admin_router.callback_query(QuestionNavigate.filter(F.button == 'amount'))
async def answers_amount(callback: CallbackQuery, callback_data: QuestionNavigate):
    answers = await requests.collect_answers(callback_data.question_id)
    await callback.answer(
        text=f'На вопрос #{callback_data.question_id} ответило: {len(answers)} гостей!',
        show_alert=True,
    )


@admin_router.callback_query(QuestionNavigate.filter(F.button == 'send'))
async def send_question(callback: CallbackQuery, callback_data: QuestionNavigate, bot: Bot):
    question_id = callback_data.question_id
    response = await requests.get_question(question_id)
    question, answers = response
    users_list = await requests.all_users()
    count_correct, count_exception = 0, 0
    for user_id in users_list:
        if user_id != config.ADMIN_TG_ID:
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=question.question,
                    reply_markup=ikb_answers(
                        user_id,
                        response,
                    ),
                )
                count_correct += 1
            except:
                await bot.send_message(
                    chat_id=callback.from_user.id,
                    text=f'Не удалось отправить: {user_id}',
                )
                count_exception += 1
    await callback.answer(
        text=f'Успешно: {count_correct}\nНе отправлено: {count_exception}',
        show_alert=True,
    )
