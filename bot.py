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

# Получаем токен бота из переменных окружения
# На Render это обычно устанавливается как "KEY" или "BOT_TOKEN" в настройках
TOKEN = os.getenv("BOT_TOKEN") # Изменено с "KEY" на "BOT_TOKEN" для ясности

# URL вашего FastAPI сервиса на Render, который будет отдавать Web App
# ЭТУ ССЫЛКУ НУЖНО БУДЕТ ЗАМЕНИТЬ НА РЕАЛЬНЫЙ URL ВАШЕГО РАЗВЕРНУТОГО FastAPI-СЕРВИСА НА RENDER!
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://cs-1-5db8.onrender.com") # Пример

# Убедитесь, что токен доступен
if not TOKEN:
    logging.error("Telegram Bot Token (BOT_TOKEN) not found in environment variables.")
    exit(1)

# Инициализация бота с новыми настройками по умолчанию для aiogram 3.x
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Этот хэндлер отвечает на команду /start и предлагает открыть Web App.
    """
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎲 Открыть рулетку",
                    web_app=WebAppInfo(url=f"{WEB_APP_URL}/") # Ссылка на корень FastAPI, который отдает index.html
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
    # Запускаем все зарегистрированные хэндлеры
    logging.info("Starting bot polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
