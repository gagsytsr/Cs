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

class User:
    def __init__(self, user_id: int, balance: int = 100):
        self.user_id = user_id
        self.balance = balance
        self.inventory = [] # Просто список имен скинов

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
        users[user_id] = User(user_id) # Создаем нового пользователя, если не существует
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
