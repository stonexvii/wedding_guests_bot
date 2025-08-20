from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from .admin_router import start_wedding
from classes import push_message, FileManager
from database import requests
from keyboards import ikb_show_answer
from keyboards.callback_data import UserAnswer, ShowAnswer

inline_router = Router()


@inline_router.callback_query(ShowAnswer.filter(F.button == 'target'))
async def questions_results(callback: CallbackQuery, callback_data: ShowAnswer, state: FSMContext, bot: Bot):
    data = await state.get_data()
    json_data = data['json']
    answers_dict = data['answers_dict']
    answers_list = data['answers_list']
    answers_list.remove((callback_data.position, callback_data.target_answer, callback_data.answer_amount))
    json_data[
        f'answer_{callback_data.position}'] = f'{callback_data.answer_amount}: {answers_dict[callback_data.target_answer]}'
    await state.update_data(answers_list=answers_list, json=json_data)
    push_message(json_data)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=data['text'],
        reply_markup=ikb_show_answer(answers_list, answers_dict),
    )


@inline_router.callback_query(ShowAnswer.filter(), ShowAnswer.filter(F.button == 'reset'))
async def clear_answers(callback: CallbackQuery, callback_data: ShowAnswer, state: FSMContext, bot: Bot):
    json_data = {
        'question': await FileManager.read('cap'),
        'answer_1': '',
        'answer_2': '',
        'answer_3': '',
        'answer_4': '',
    }
    push_message(json_data)
    await callback.answer(
        text='Вывод очищен!',
        show_alert=True,
    )
    await state.clear()
    await start_wedding(callback, bot)


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
