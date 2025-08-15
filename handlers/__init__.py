from aiogram import Router

from .command_router import command_router
from .admin_router import admin_router
from .inline_router import inline_router

main_router = Router()

main_router.include_routers(
    command_router,
    inline_router,
    admin_router,
)
