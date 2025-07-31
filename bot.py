import os
import asyncio
import logging # Для логирования, очень полезно для отладки

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import threading

# Настройка логирования для отладки
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Загрузка токена из переменных окружения
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    logger.error("BOT_TOKEN environment variable not set. Please set it on Render.")
    # В production лучше поднять исключение или выйти, но для отладки можно так
    # raise ValueError("BOT_TOKEN environment variable not set.")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Создание FastAPI приложения
app = FastAPI()

# Отдача главной страницы Web App
@app.get("/", response_class=HTMLResponse)
async def get_webapp():
    try:
        # Проверяем наличие файла перед отправкой
        if not os.path.exists('index.html'):
            logger.error("index.html not found!")
            return HTMLResponse("<h1>Error: index.html not found on server.</h1>", status_code=404)
        return FileResponse('index.html')
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        return HTMLResponse(f"<h1>Server Error: {e}</h1>", status_code=500)

# Отдача статики (css, js, изображения)
@app.get("/assets/{file_path:path}")
async def get_assets(file_path: str):
    full_path = f'assets/{file_path}'
    try:
        # Проверяем наличие файла перед отправкой
        if not os.path.exists(full_path):
            logger.warning(f"File not found: {full_path}")
            return HTMLResponse(f"<h1>Error: File not found: {file_path}</h1>", status_code=404)
        return FileResponse(full_path)
    except Exception as e:
        logger.error(f"Error serving asset {file_path}: {e}")
        return HTMLResponse(f"<h1>Server Error serving asset: {e}</h1>", status_code=500)

# Отдача других статических файлов из корня (если нужны)
@app.get("/{file_path:path}")
async def get_static_files(file_path: str):
    # Этот эндпоинт может быть потенциально опасен, если не контролировать
    #, к каким файлам он дает доступ. Для Web App обычно достаточно /assets/
    # Рекомендуется использовать его только для явно необходимых статических файлов в корне.
    if file_path in ['style.css', 'script.js']: # Явно разрешаем только эти
        try:
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                return HTMLResponse(f"<h1>Error: File not found: {file_path}</h1>", status_code=404)
            return FileResponse(file_path)
        except Exception as e:
            logger.error(f"Error serving static file {file_path}: {e}")
            return HTMLResponse(f"<h1>Server Error serving static file: {e}</h1>", status_code=500)
    else:
        logger.warning(f"Attempted to access restricted file: {file_path}")
        return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)


# Обработка команды /start для aiogram 3.x
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    # !!! ВАЖНО: ЗАМЕНИТЕ ЭТОТ URL НА РЕАЛЬНЫЙ URL, КОТОРЫЙ ВЫ ПОЛУЧИТЕ ОТ RENDER !!!
    # Пример: "https://your-service-name.onrender.com"
    render_webapp_url = os.getenv('RENDER_WEBAPP_URL', "https://cs-1-870u.onrender.com") # Сделаем его переменной окружения
    if render_webapp_url == "https://example.com":
        logger.warning("RENDER_WEBAPP_URL environment variable not set. Using placeholder URL.")

    # Создание ReplyKeyboardMarkup с WebAppInfo
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🎲 Открыть рулетку",
                    web_app=WebAppInfo(url=render_webapp_url)
                )
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🎁 Открыть кейсы 🎁",
        reply_markup=keyboard
    )
    logger.info(f"Sent start message to user {message.from_user.id}")


# Функция для запуска FastAPI в отдельном потоке
def start_web_server():
    """Запускает Uvicorn-сервер для FastAPI в отдельном потоке."""
    port = int(os.getenv('PORT', 8000))
    logger.info(f"Starting Uvicorn web server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

# Главная точка входа, запускающая бота и веб-сервер
async def main() -> None:
    logger.info("Starting bot and web server...")

    # Запускаем FastAPI в отдельном потоке
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    logger.info("Web server thread started.")

    # Запускаем бота на Long Polling
    try:
        await dp.start_polling(bot)
        logger.info("Bot polling started.")
    except Exception as e:
        logger.error(f"Error starting bot polling: {e}")

if __name__ == "__main__":
    asyncio.run(main())

