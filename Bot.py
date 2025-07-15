import os
from aiogram import Bot, Dispatcher, executor, types
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
import threading

# Загрузка токена из переменных окружения
TOKEN = os.getenv('BOT_TOKEN')

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Создание FastAPI приложения
app = FastAPI()

# Отдача главной страницы Web App
@app.get("/")
async def get_webapp():
    return FileResponse('index.html')

# Отдача статики (css, js, изображения)
@app.get("/assets/{file_path:path}")
async def get_assets(file_path: str):
    return FileResponse(f'assets/{file_path}')

@app.get("/{file_path:path}")
async def get_static_files(file_path: str):
    return FileResponse(file_path)

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "🎁 Открыть кейсы 🎁",
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(
                "🎲 Открыть рулетку",
                web_app=types.WebAppInfo("https://твой-домен.onrender.com")  # замени на реальную ссылку
            )
        )
    )

# Запуск FastAPI и бота одновременно
if __name__ == "__main__":
    def start_web():
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 8000)))

    threading.Thread(target=start_web).start()
    executor.start_polling(dp)
