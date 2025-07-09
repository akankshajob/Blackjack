const lobby = document.getElementById('lobby');
const game = document.getElementById('game');
const joinBtn = document.getElementById('joinBtn');
const addBotBtn = document.getElementById('addBotBtn');
const startBtn = document.getElementById('startBtn');
const hitBtn = document.getElementById('hitBtn');
const standBtn = document.getElementById('standBtn');
const backBtn = document.getElementById('backBtn');
const playerNameInput = document.getElementById('playerName');
const roomIdInput = document.getElementById('roomId');
const messages = document.getElementById('messages');
const roomTitle = document.getElementById('roomTitle');
const dealerArea = document.getElementById('dealerArea');
const playersArea = document.getElementById('playersArea');
const funFact = document.getElementById('funFact');

let ws = null;
let myName = '';
let myRoom = '';
let lastState = null;

const SUIT_EMOJI = {
    'Hearts': '♥️',
    'Diamonds': '♦️',
    'Clubs': '♣️',
    'Spades': '♠️',
    'Hidden': '🂠'
};
const AVATAR_EMOJI = ['🦄','🐱','🐶','🦊','🐸','🐵','🐼','🐯','🐨','🐰','🦁','🐮','🐷','🐙','🐧','🐤','🦉','🦋','🐝','🦄','🐲','🦖','🦕','🦓','🦒','🦘','🦥','🦦','🦨','🦡','🦔','🐾'];
const FUN_FACTS = [
    "Blackjack is also called 21!",
    "Aces can be worth 1 or 11 points.",
    "The dealer must hit until reaching 17.",
    "You can play with friends or bots!",
    "Try to beat the dealer without going over 21!",
    "Blackjack pays 3:2 in casinos.",
    "The best hand is an Ace and a 10-value card!",
    "Bots play with a simple strategy. Can you outsmart them?",
    "You can add as many bots as you want!",
    "Have fun and good luck! 🍀"
];

function randomAvatar(name) {
    // Deterministic avatar based on name
    let hash = 0;
    for (let i = 0; i < name.length; i++) hash += name.charCodeAt(i);
    return AVATAR_EMOJI[hash % AVATAR_EMOJI.length];
}

function showFunFact() {
    funFact.textContent = FUN_FACTS[Math.floor(Math.random() * FUN_FACTS.length)];
}
showFunFact();
funFact.onclick = showFunFact;

function renderCard(card) {
    if (card.rank === 'Hidden') return `<span class="card">🂠</span>`;
    return `<span class="card">${card.rank}${SUIT_EMOJI[card.suit]}</span>`;
}

function renderHand(hand) {
    return hand.map(renderCard).join(' ');
}

function renderPlayers(players, turn) {
    return players.map(p => {
        let turnMark = (turn === p.name) ? '👉 ' : '';
        let botMark = p.is_bot ? '🤖' : '';
        let bust = p.bust ? '💥' : '';
        let stand = p.stand ? '🛑' : '';
        let avatar = randomAvatar(p.name);
        return `<div class="playerRow">${turnMark}<span class="avatar">${avatar}</span> <b>${p.name}</b> ${botMark} ${bust}${stand}<br>${renderHand(p.hand)}<br><span class="score">${p.value !== '?' ? 'Score: ' + p.value : ''}</span></div>`;
    }).join('');
}

function renderDealer(dealer) {
    return `<div class="dealerRow"><span class="avatar">🃏</span> <b>Dealer</b><br>${renderHand(dealer.hand)}<br><span class="score">${dealer.value !== '?' ? 'Score: ' + dealer.value : ''}</span></div>`;
}

joinBtn.onclick = () => {
    myName = playerNameInput.value.trim();
    myRoom = roomIdInput.value.trim();
    if (!myName || !myRoom) return alert('Enter your name and room ID!');
    ws = new WebSocket(`ws://127.0.0.1:8000/ws/${myRoom}/${myName}`);
    ws.onopen = () => {
        lobby.style.display = 'none';
        game.style.display = '';
        roomTitle.textContent = `Room: ${myRoom}`;
        addBotBtn.style.display = '';
    };
    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.type === 'state') {
            lastState = msg.state;
            updateGameUI(msg.state);
        }
    };
    ws.onclose = () => {
        alert('Disconnected from server.');
        location.reload();
    };
};

backBtn.onclick = () => {
    if (ws) ws.close();
    game.style.display = 'none';
    lobby.style.display = '';
    showFunFact();
    playerNameInput.value = '';
    roomIdInput.value = '';
    messages.innerHTML = '';
    dealerArea.innerHTML = '';
    playersArea.innerHTML = '';
};

addBotBtn.onclick = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({action: 'add_bot'}));
    }
};

startBtn.onclick = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({action: 'start'}));
    }
};

hitBtn.onclick = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({action: 'hit'}));
    }
};

standBtn.onclick = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({action: 'stand'}));
    }
};

function updateGameUI(state) {
    // Dealer
    dealerArea.innerHTML = renderDealer(state.dealer);
    // Players
    playersArea.innerHTML = renderPlayers(state.players, state.turn);
    // Actions
    if (!state.started) {
        startBtn.style.display = '';
        hitBtn.style.display = 'none';
        standBtn.style.display = 'none';
        messages.innerHTML = '<span class="waiting">Waiting for players... Add friends or bots and start the game!</span>';
    } else if (state.over) {
        startBtn.style.display = '';
        hitBtn.style.display = 'none';
        standBtn.style.display = 'none';
        showWinners(state);
    } else {
        startBtn.style.display = 'none';
        // Only show Hit/Stand if it's your turn and you're not a bot
        const me = state.players.find(p => p.name === myName);
        if (state.turn === myName && me && !me.stand && !me.bust && !me.is_bot) {
            hitBtn.style.display = '';
            standBtn.style.display = '';
        } else {
            hitBtn.style.display = 'none';
            standBtn.style.display = 'none';
        }
        messages.innerHTML = '';
    }
}

function showWinners(state) {
    let dealerScore = state.dealer.value === '?' ? 0 : state.dealer.value;
    let dealerBust = state.dealer.bust;
    let msg = '<b>Game Over!</b><br>';
    let winner = null;
    let maxScore = 0;
    state.players.forEach(p => {
        if (p.bust) {
            msg += `${randomAvatar(p.name)} ${p.name}: BUST! Dealer wins.<br>`;
        } else if (dealerBust || p.value > dealerScore) {
            msg += `${randomAvatar(p.name)} ${p.name}: 🎉 You win!<br>`;
            if (p.value > maxScore) { winner = p.name; maxScore = p.value; }
        } else if (p.value === dealerScore) {
            msg += `${randomAvatar(p.name)} ${p.name}: 🤝 Push (tie).<br>`;
        } else {
            msg += `${randomAvatar(p.name)} ${p.name}: Dealer wins.<br>`;
        }
    });
    messages.innerHTML = msg;
    if (winner) confetti();
}

// Simple confetti animation
function confetti() {
    for (let i = 0; i < 30; i++) {
        let conf = document.createElement('div');
        conf.className = 'confetti';
        conf.style.left = Math.random() * 100 + 'vw';
        conf.style.background = `hsl(${Math.random()*360},90%,60%)`;
        conf.style.animationDuration = (1 + Math.random() * 1.5) + 's';
        document.body.appendChild(conf);
        setTimeout(() => conf.remove(), 2000);
    }
} 