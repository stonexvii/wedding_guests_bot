from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from classes import FileManager
from database import requests

command_router = Router()


@command_router.message(Command('start'))
async def command_start(message: Message):
    message_text = await FileManager.read('intro')
    await requests.add_user(
        message.from_user.id,
        str(message.from_user.username),
    )
    await message.answer(
        text=message_text,
    )
