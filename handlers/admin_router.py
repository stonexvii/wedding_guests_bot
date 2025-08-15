from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

import config
from classes import FileManager
from database import requests
from .fsm_states import ShowAnswer
from keyboards import ikb_answers, ikb_show_answer
from middlewares import AdminMiddleware

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.message(Command('all'))
async def all_question(message: Message):
    msg_text = ''
    quest_data = await requests.all_questions()
    quest_data = sorted(quest_data, key=lambda x: x.id)
    for question in quest_data:
        answers = await requests.all_question_answers(question.id)
        msg_text += f'#{question.id} {question.question}\n'
        for answer in answers:
            msg_text += f'\t{answer.answer_id}: {answer.answer}\n'
        msg_text += '\n'
    await message.answer(
        text=msg_text,
    )


@admin_router.message(Command('write'))
async def command_write(message: Message, command: CommandObject):
    file_name, data = command.args.split(' ', 1)
    await FileManager.write(file_name, data)


@admin_router.message(Command('set'))
async def command_set(message: Message, command: CommandObject):
    question_id, question_data = command.args.split(' ', 1)
    question, *answers = question_data.split('\n')
    await requests.set_question(
        question_id=int(question_id),
        question_text=question,
        answers=answers,
    )


@admin_router.message(Command('del'))
async def command_set(message: Message, command: CommandObject):
    question_id = int(command.args)
    await requests.delete_question(
        question_id=question_id,
    )


@admin_router.message(Command('show'))
async def show_answers(message: Message, command: CommandObject, state: FSMContext, bot: Bot):
    await state.set_state(ShowAnswer.next_answer)
    question_id = int(command.args)
    quest_data = await requests.get_question(question_id)
    question, answers = quest_data
    answers_dict = {answer.answer_id: answer.answer for answer in answers}
    user_answers = await requests.collect_answers(question_id)
    total_answers = len(user_answers)
    answers_count = {ans.answer_id: user_answers.count(ans.answer_id) for ans in answers}
    answers_list = sorted(list(answers_count.items()), key=lambda x: x[1], reverse=True)
    msg_txt = f'{question.question}\n'
    if answers:
        for answer in answers:
            count = answers_count[answer.answer_id]
            msg_txt += f'\t{count} {answer.answer}\n'
    await message.answer(
        text=msg_txt,
        reply_markup=ikb_show_answer(answers_list, answers_dict),
    )
    await state.set_data({
        'answers_list': answers_list,
        'answers_dict': answers_dict,
        'text': msg_txt,
        'question': question.question,
        'messages_id': [],
    })


@admin_router.message()
async def send_question(message: Message, bot: Bot):
    question_id = int(message.text)
    response = await requests.get_question(question_id)
    if response:
        question, answers = response
        users_list = await requests.all_users()
        for user_id in users_list:
            if user_id not in (config.ADMIN_TG_ID, config.MONITOR_TG_ID):
                try:
                    await bot.send_message(
                        chat_id=user_id,
                        text=question.question,
                        reply_markup=ikb_answers(
                            message.from_user.id,
                            response,
                        ),
                    )
                except:
                    print(f'Не удалось отправить: {user_id}')
    else:
        await message.answer(
            text=f'Вопроса №{question_id} не существует!'
        )
