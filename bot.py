import asyncio
import logging
import os
from threading import Thread

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.client.default import DefaultBotProperties

# >>> Добавлены импорты для FastAPI <<<
from fastapi import FastAPI
import uvicorn
# >>> Конец добавленных импортов <<<

# Конфигурация логирования
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
# >>> WEB_APP_URL теперь жестко прописан в коде <<<
WEB_APP_URL = "https://cs-2.onrender.com"

if not TOKEN:
    logging.error("Telegram Bot Token (BOT_TOKEN) not found in environment variables.")
    exit(1)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# --- Код вашего бота ---
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # Здесь используется жестко прописанный WEB_APP_URL
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎲 Открыть рулетку",
                    web_app=WebAppInfo(url=f"{WEB_APP_URL}/") # Используем f-строку для добавления слэша
                )
            ]
        ]
    )
    await message.answer(
        f"Привет, {message.from_user.full_name}! Нажми кнопку, чтобы открыть кейсы:",
        reply_markup=markup
    )

# >>> Дополнительный FastAPI для "держания порта открытым" <<<
web_app = FastAPI()

@web_app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Bot is alive and listening."}

# Функция для запуска FastAPI в отдельном потоке
def run_fastapi_server():
    port = int(os.getenv('PORT', 8000))
    logging.info(f"Starting FastAPI health check server on port {port}")
    uvicorn.run(web_app, host="0.0.0.0", port=port)

# --- Основная функция запуска (теперь с FastAPI в потоке) ---
async def main() -> None:
    # Удаление старых вебхуков (оставить для первого запуска, потом можно удалить)
    logging.info("Deleting old webhooks...")
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Webhook deleted. Starting bot polling...")

    # Запускаем FastAPI сервер в отдельном потоке
    Thread(target=run_fastapi_server, daemon=True).start()
    logging.info(f"FastAPI health check server started on port {os.getenv('PORT', 8000)}")

    # Запускаем Long Polling бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
