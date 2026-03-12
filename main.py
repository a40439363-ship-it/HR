import asyncio
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN, ADMIN_CHAT_ID, EXCEL_FILE
from bot.handlers import router


async def main():
    print("Admin chat id:", ADMIN_CHAT_ID)
    print("Excel file:", EXCEL_FILE)

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN topilmadi. .env faylni tekshiring.")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    me = await bot.get_me()
    print("Bot ishga tushdi:", f"@{me.username}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
