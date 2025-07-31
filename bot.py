import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties # Добавлен этот импорт

# Конфигурация логирования
logging.basicConfig(level=logging.INFO)

# Получаем токен бота из переменных окружения
# На Render это обычно устанавливается как "KEY" в настройках
TOKEN = os.getenv("KEY")

# Убедитесь, что токен доступен
if not TOKEN:
    logging.error("Telegram Bot Token (KEY) not found in environment variables.")
    exit(1)

# Инициализация бота с новыми настройками по умолчанию
# ВАЖНО: ParseMode.HTML теперь передается через DefaultBotProperties
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # Изменена эта строка
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Этот хэндлер отвечает на команду /start.
    """
    await message.answer(f"Привет, {message.from_user.full_name}!")

# Основная функция запуска бота
async def main() -> None:
    # Запускаем все зарегистрированные хэндлеры
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
