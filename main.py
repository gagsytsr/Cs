# main.py (ваш текущий main.py без логики бота и без @app.on_event("startup") и asyncio.create_task(start_bot()))
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import random
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# 1. Отдача статических файлов (HTML, CSS, JS, Images)
# Убедитесь, что папка 'public' существует в корне вашего проекта
app.mount("/public", StaticFiles(directory="public"), name="public")

# Отдача главной страницы mini-app (index.html)
@app.get("/", response_class=HTMLResponse)
async def serve_webapp_index():
    return FileResponse(os.path.join("public", "index.html"))

# --- Игровая логика (очень упрощенная пока) ---
# В реальном приложении это должно быть в базе данных!

class User(BaseModel): # Добавим BaseModel для корректной работы pydantic
    user_id: int
    balance: int = 100
    inventory: list = [] # Просто список имен скинов

# Временное хранилище пользователей (в памяти, исчезнет при перезапуске)
users = {}

# Пример скинов (в реальном приложении - из базы данных)
SKINS = [
    {"name": 'AWP Asiimov', "image": 'awp_asiimov.png', "rarity": "rare", "price": 50},
    {"name": 'AK-47 Redline', "image": 'ak_redline.png', "rarity": "rare", "price": 40},
    {"name": 'M4A4 Howl', "image": 'm4a4_howl.png', "rarity": "legendary", "price": 200},
    {"name": 'Glock-18 Fade', "image": 'glock_fade.png', "rarity": "epic", "price": 80},
    {"name": 'Deagle Blaze', "image": 'deagle_blaze.png', "rarity": "uncommon", "price": 20},
    {"name": 'USP-S Printstream', "image": 'usp_printstream.png', "rarity": "rare", "price": 60},
    {"name": 'Karambit Doppler', "image": 'karambit_doppler.png', "rarity": "mythical", "price": 300},
]

# Вероятности выпадения скинов (просто пример, для реальной игры нужно доработать)
RARITY_PROBABILITIES = {
    "uncommon": 0.4,
    "rare": 0.3,
    "epic": 0.15,
    "legendary": 0.1,
    "mythical": 0.05,
}

# Вспомогательная функция для выбора скина по вероятности
def get_random_skin():
    rand_val = random.random()
    current_prob = 0
    for rarity, prob in RARITY_PROBABILITIES.items():
        current_prob += prob
        if rand_val <= current_prob:
            possible_skins = [s for s in SKINS if s["rarity"] == rarity]
            if possible_skins:
                return random.choice(possible_skins)
    # Fallback in case something goes wrong with probabilities
    return random.choice(SKINS)


# API для получения информации о пользователе
@app.get("/api/user/{user_id}", response_model=User)
async def get_user_info(user_id: int):
    if user_id not in users:
        users[user_id] = User(user_id=user_id) # Создаем нового пользователя, если не существует
    return users[user_id]

# API для открытия кейса
@app.post("/api/open_case/{user_id}")
async def open_case(user_id: int):
    COST_PER_SPIN = 30
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    user = users[user_id]
    if user.balance < COST_PER_SPIN:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    user.balance -= COST_PER_SPIN
    won_skin = get_random_skin()
    user.inventory.append(won_skin["name"]) # Добавляем имя скина в инвентарь
    logging.info(f"User {user_id} opened case. Won: {won_skin['name']}. New balance: {user.balance}")
    return {"status": "success", "won_skin": won_skin, "new_balance": user.balance}

# API для получения списка всех скинов (для фронтенда)
@app.get("/api/skins")
async def get_all_skins():
    return {"skins": SKINS}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if not WEB_APP_URL:
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

async def start_bot():
    if TOKEN:
        logging.info("Deleting old webhooks...")
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("Webhook deleted. Starting bot polling...")
        await dp.start_polling(bot)
    else:
        logging.warning("BOT_TOKEN not set. Telegram bot will not start.")
# --- Конец кода бота ---

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/", response_class=HTMLResponse)
async def serve_webapp_index():
    return FileResponse(os.path.join("public", "index.html"))

# ... (Весь остальной код FastAPI, User, SKINS, API-endpoints) ...

# API для получения информации о пользователе
class User(BaseModel): # Добавим BaseModel для корректной работы pydantic
    user_id: int
    balance: int = 100
    inventory: list = [] # Просто список имен скинов

# Временное хранилище пользователей (в памяти, исчезнет при перезапуске)
users = {}

# Пример скинов (в реальном приложении - из базы данных)
SKINS = [
    {"name": 'AWP Asiimov', "image": 'awp_asiimov.png', "rarity": "rare", "price": 50},
    {"name": 'AK-47 Redline', "image": 'ak_redline.png', "rarity": "rare", "price": 40},
    {"name": 'M4A4 Howl', "image": 'm4a4_howl.png', "rarity": "legendary", "price": 200},
    {"name": 'Glock-18 Fade', "image": 'glock_fade.png', "rarity": "epic", "price": 80},
    {"name": 'Deagle Blaze', "image": 'deagle_blaze.png', "rarity": "uncommon", "price": 20},
    {"name": 'USP-S Printstream', "image": 'usp_printstream.png', "rarity": "rare", "price": 60},
    {"name": 'Karambit Doppler', "image": 'karambit_doppler.png', "rarity": "mythical", "price": 300},
]

# Вероятности выпадения скинов (просто пример, для реальной игры нужно доработать)
RARITY_PROBABILITIES = {
    "uncommon": 0.4,
    "rare": 0.3,
    "epic": 0.15,
    "legendary": 0.1,
    "mythical": 0.05,
}

# Вспомогательная функция для выбора скина по вероятности
def get_random_skin():
    rand_val = random.random()
    current_prob = 0
    for rarity, prob in RARITY_PROBABILITIES.items():
        current_prob += prob
        if rand_val <= current_prob:
            possible_skins = [s for s in SKINS if s["rarity"] == rarity]
            if possible_skins:
                return random.choice(possible_skins)
    # Fallback in case something goes wrong with probabilities
    return random.choice(SKINS)


@app.get("/api/user/{user_id}", response_model=User)
async def get_user_info(user_id: int):
    if user_id not in users:
        users[user_id] = User(user_id=user_id) # Создаем нового пользователя, если не существует
    return users[user_id]

# API для открытия кейса
@app.post("/api/open_case/{user_id}")
async def open_case(user_id: int):
    COST_PER_SPIN = 30
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    user = users[user_id]
    if user.balance < COST_PER_SPIN:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    user.balance -= COST_PER_SPIN
    won_skin = get_random_skin()
    user.inventory.append(won_skin["name"]) # Добавляем имя скина в инвентарь
    logging.info(f"User {user_id} opened case. Won: {won_skin['name']}. New balance: {user.balance}")
    return {"status": "success", "won_skin": won_skin, "new_balance": user.balance}

# API для получения списка всех скинов (для фронтенда)
@app.get("/api/skins")
async def get_all_skins():
    return {"skins": SKINS}


# Основная точка входа для запуска обоих сервисов
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot()) # Запускаем бота как фоновую задачу

if __name__ == "__main__":
    # Uvicorn будет запущен на порту, предоставленном Pella.app
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
