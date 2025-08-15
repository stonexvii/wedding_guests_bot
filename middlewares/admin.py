from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Callable, Dict, Any, Awaitable

import config


class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id == config.ADMIN_TG_ID:
            result = await handler(event, data)
            return result
