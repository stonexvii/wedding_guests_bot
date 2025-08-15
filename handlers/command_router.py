from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import config
from classes import FileManager
from database import requests
from keyboards import ikb_answers

command_router = Router()


@command_router.message(Command('start'))
async def command_start(message: Message, bot: Bot):
    message_text = await FileManager.read('intro')
    await requests.add_user(
        message.from_user.id,
        str(message.from_user.username),
    )
    await message.answer(
        text=message_text,
    )






