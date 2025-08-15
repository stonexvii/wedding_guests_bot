from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import config
from database import requests
# from .fsm_states import ShowAnswer
from keyboards import ikb_show_answer
from keyboards.callback_data import UserAnswer, ShowAnswer, QuestionNavigate

inline_router = Router()


@inline_router.callback_query(ShowAnswer.filter(F.button == 'target'))
async def questions_results(callback: CallbackQuery, callback_data: ShowAnswer, state: FSMContext, bot: Bot):
    data = await state.get_data()
    answers_dict = data['answers_dict']
    answers_list = data['answers_list']
    answers_list.remove((callback_data.target_answer, callback_data.answer_amount))
    out_message = await bot.send_message(
        chat_id=config.MONITOR_TG_ID,
        text=f'{data['question']}\n{answers_dict[callback_data.target_answer]} {callback_data.answer_amount}',
    )
    out_messages = await state.get_value('messages_id')
    out_messages.append(out_message.message_id)
    await state.update_data(messages_id=out_messages, answers_list=answers_list)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=data['text'],
        reply_markup=ikb_show_answer(answers_list, answers_dict),
    )


@inline_router.callback_query(ShowAnswer.filter(), ShowAnswer.filter(F.button == 'reset'))
async def show_answer(callback: CallbackQuery, callback_data: ShowAnswer, state: FSMContext, bot: Bot):
    data = await state.get_data()
    for message_id in data['messages_id']:
        await bot.delete_message(
            chat_id=config.MONITOR_TG_ID,
            message_id=message_id,
        )
    await callback.answer(
        text='Вывод очищен!',
        show_alert=True,
    )
    await state.clear()


@inline_router.callback_query(UserAnswer.filter())
async def user_answer_handler(callback: CallbackQuery, callback_data: UserAnswer, bot: Bot):
    await requests.add_user_answer(
        callback_data.user_id,
        callback_data.question_id,
        callback_data.answer_id,
    )
    await callback.answer(
        text='Ваш ответ принят!',
        show_alert=True,
    )
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
    )
