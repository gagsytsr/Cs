const roulette = document.getElementById('roulette');
const spinBtn = document.getElementById('spin-btn');
const resultText = document.getElementById('result-text');
const balanceText = document.getElementById('balance-text');

let balance = 100;

const skins = [
    { name: 'AWP Asiimov', image: 'awp_asiimov.png' },
    { name: 'AK-47 Redline', image: 'ak_redline.png' },
    { name: 'M4A4 Howl', image: 'm4a4_howl.png' },
    { name: 'Glock-18 Fade', image: 'glock_fade.png' },
    { name: 'Deagle Blaze', image: 'deagle_blaze.png' }
];

function updateBalance() {
    balanceText.innerText = `Баланс: ${balance}⭐`;
}

function createRouletteItems() {
    roulette.innerHTML = '';
    for (let i = 0; i < 40; i++) {
        const skin = skins[Math.floor(Math.random() * skins.length)];
        const div = document.createElement('div');
        div.className = 'item';
        div.innerHTML = `
            <img src="assets/skins/${skin.image}" style="width:80px; height:80px; display:block; margin:10px auto;">
            <span style="font-size:12px; color:white;">${skin.name}</span>
        `;
        roulette.appendChild(div);
    }
}

function spinRoulette() {
    if (balance < 30) {
        alert('Недостаточно звёзд!');
        return;
    }

    balance -= 30;
    updateBalance();
    resultText.innerText = '';

    createRouletteItems();
    roulette.style.transition = 'transform 3s ease-out';
    roulette.style.transform = `translateX(-${Math.random() * 2000 + 1000}px)`;

    setTimeout(() => {
        const wonSkin = skins[Math.floor(Math.random() * skins.length)];
        resultText.innerText = `🎉 Тебе выпало: ${wonSkin.name}`;
    }, 3000);
}

spinBtn.addEventListener('click', spinRoulette);
updateBalance();
createRouletteItems();