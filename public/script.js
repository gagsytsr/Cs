const roulette = document.getElementById('roulette');
const spinBtn = document.getElementById('spin-btn');
const resultText = document.getElementById('result-text');
const balanceText = document.getElementById('balance-text');
const userId = window.Telegram.WebApp.initDataUnsafe.user.id; // Получаем ID пользователя из Telegram WebApp API

let balance = 0; // Баланс будет загружаться с бэкенда
let skins = []; // Скины будут загружаться с бэкенда

// Функция для обновления баланса на UI
function updateBalance() {
    balanceText.innerText = `Баланс: ${balance}⭐`;
}

// Загрузка данных пользователя и скинов с бэкенда
async function loadGameData() {
    try {
        // Загружаем скины
        const skinsResponse = await fetch('/api/skins');
        const skinsData = await skinsResponse.json();
        skins = skinsData.skins; // Сохраняем полученные скины

        // Загружаем данные пользователя
        const userResponse = await fetch(`/api/user/${userId}`);
        const userData = await userResponse.json();
        balance = userData.balance;
        updateBalance();
        createRouletteItems(); // Создаем элементы рулетки после загрузки скинов
    } catch (error) {
        console.error("Ошибка загрузки данных игры:", error);
        alert("Не удалось загрузить данные игры. Пожалуйста, попробуйте позже.");
    }
}


function createRouletteItems() {
    roulette.innerHTML = '';
    // Генерируем элементы рулетки из загруженных скинов
    for (let i = 0; i < 40; i++) {
        const skin = skins[Math.floor(Math.random() * skins.length)];
        const div = document.createElement('div');
        div.className = 'item';
        div.innerHTML = `
            <img src="/public/assets/skins/${skin.image}" style="width:80px; height:80px; display:block; margin:10px auto;">
            <span style="font-size:12px; color:white;">${skin.name}</span>
        `;
        roulette.appendChild(div);
    }
}

async function spinRoulette() {
    // Отправляем запрос на бэкенд для открытия кейса
    try {
        const response = await fetch(`/api/open_case/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // body: JSON.stringify({ cost: 30 }) // Если нужно передавать стоимость
        });

        const data = await response.json();

        if (response.status === 400) {
            alert(data.detail); // "Insufficient balance"
            return;
        }
        if (!response.ok) {
            throw new Error(data.detail || 'Ошибка открытия кейса');
        }

        balance = data.new_balance;
        updateBalance();
        resultText.innerText = '';

        createRouletteItems(); // Пересоздаем элементы рулетки для новой анимации
        roulette.style.transition = 'none'; // Сбрасываем переход для мгновенного сдвига
        roulette.style.transform = `translateX(0px)`; // Возвращаем в начальное положение

        // Принудительная перерисовка
        roulette.offsetWidth;

        // Определяем, какой скин выпал, чтобы остановить рулетку на нем
        const wonSkin = data.won_skin;
        const targetIndex = skins.findIndex(s => s.name === wonSkin.name); // Найдем индекс выпавшего скина

        // Двигаем рулетку так, чтобы выпавший скин оказался в центре
        // Это требует более сложной логики позиционирования,
        // пока просто случайное смещение, но можно доработать.
        // Для точного позиционирования нужна ширина элемента и точное смещение.
        const itemWidth = 140; // Ширина .item + margin, примерно
        const offsetToCenter = roulette.offsetWidth / 2 - itemWidth / 2; // Смещение для центрирования

        const desiredOffset = -(targetIndex * itemWidth) + offsetToCenter + (Math.random() * itemWidth - itemWidth / 2); // Смещение к нужному элементу с небольшой рандомизацией

        roulette.style.transition = 'transform 3s cubic-bezier(0.25, 0.1, 0.25, 1)'; // Плавная анимация
        roulette.style.transform = `translateX(${desiredOffset}px)`; // Двигаем к нужному скину

        setTimeout(() => {
            resultText.innerText = `🎉 Тебе выпало: ${wonSkin.name}`;
            // Можно добавить Telegram.WebApp.HapticFeedback.impactOccurred('light');
        }, 3000);

    } catch (error) {
        console.error('Ошибка при кручении рулетки:', error);
        alert(`Ошибка: ${error.message}`);
    }
}

spinBtn.addEventListener('click', spinRoulette);

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    // Инициализация Telegram WebApp API
    if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();
        loadGameData();
    } else {
        // Для локальной отладки без Telegram WebApp
        console.warn("Telegram WebApp API не инициализирован. Запускаем с тестовым user_id.");
        // Test user_id for local development
        // You'll need to mock window.Telegram.WebApp.initDataUnsafe.user.id for local testing
        // For actual deployment, this will be provided by Telegram.
        // For now, let's hardcode a dummy user_id if not in Telegram environment
        if (!userId) {
            console.error("User ID not available. Mini-app might not function correctly outside Telegram.");
            // Example for local test: userId = 123;
        }
        loadGameData();
    }
});
