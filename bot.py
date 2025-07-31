# bot.py (ваш оригинальный bot.py)
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.client.default import DefaultBotProperties

# Конфигурация логирования
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://your-fastapi-service.onrender.com") # Это будет URL вашего Heroku-приложения

if not TOKEN:
    logging.error("Telegram Bot Token (BOT_TOKEN) not found in environment variables.")
    exit(1)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if not WEB_APP_URL: # Добавим проверку на всякий случай
        await message.answer("Ошибка: WEB_APP_URL не настроен. Пожалуйста, обратитесь к администратору.")
        return

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎲 Открыть рулетку",
                    web_app=WebAppInfo(url=f"{WEB_APP_URL}/")
                )
            ]
        ]
    )
    await message.answer(
        f"Привет, {message.from_user.full_name}! Нажми кнопку, чтобы открыть кейсы:",
        reply_markup=markup
    )

# Основная функция запуска бота
async def main() -> None:
    logging.info("Deleting old webhooks...")
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Webhook deleted. Starting bot polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
