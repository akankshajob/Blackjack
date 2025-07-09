from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import uvicorn
import random
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERS_FILE = "users.json"
AVATAR_EMOJI = ['🦄','🐱','🐶','🦊','🐸','🐵','🐼','🐯','🐨','🐰','🦁','🐮','🐷','🐙','🐧','🐤','🦉','🦋','🐝','🐲','🦖','🦕','🦓','🦒','🦘','🦥','🦦','🦨','🦡','🦔','🐾']

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

@app.post("/api/signup")
async def signup(data: Request):
    body = await data.json()
    username = body.get('username')
    password = body.get('password')
    avatar = body.get('avatar')
    users = load_users()
    if username in users:
        return JSONResponse({"ok": False, "error": "Username already exists."}, status_code=400)
    if not avatar:
        avatar = random.choice(AVATAR_EMOJI)
    users[username] = {"password": password, "avatar": avatar, "wins": 0, "losses": 0}
    save_users(users)
    return {"ok": True, "username": username, "avatar": avatar, "wins": 0, "losses": 0}

@app.post("/api/login")
async def login(data: Request):
    body = await data.json()
    username = body.get('username')
    password = body.get('password')
    users = load_users()
    if username not in users or users[username]['password'] != password:
        return JSONResponse({"ok": False, "error": "Invalid username or password."}, status_code=400)
    u = users[username]
    return {"ok": True, "username": username, "avatar": u['avatar'], "wins": u['wins'], "losses": u['losses']}

@app.get("/api/profile")
async def profile(username: str):
    users = load_users()
    if username not in users:
        return JSONResponse({"ok": False, "error": "User not found."}, status_code=404)
    u = users[username]
    return {"ok": True, "username": username, "avatar": u['avatar'], "wins": u['wins'], "losses": u['losses']}

@app.post("/api/score")
async def update_score(data: Request):
    body = await data.json()
    username = body.get('username')
    win = body.get('win')
    users = load_users()
    if username not in users:
        return JSONResponse({"ok": False, "error": "User not found."}, status_code=404)
    if win:
        users[username]['wins'] += 1
    else:
        users[username]['losses'] += 1
    save_users(users)
    return {"ok": True, "wins": users[username]['wins'], "losses": users[username]['losses']}

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        if self.rank == 'A':
            return 11
        return int(self.rank)
    def to_dict(self):
        return {'rank': self.rank, 'suit': self.suit}

class Player:
    def __init__(self, name, is_bot=False):
        self.name = name
        self.hand: List[Card] = []
        self.stand = False
        self.bust = False
        self.is_bot = is_bot
    def hand_value(self):
        value = sum(card.value() for card in self.hand)
        aces = sum(1 for card in self.hand if card.rank == 'A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value
    def to_dict(self, hide_first_card=False):
        if hide_first_card:
            return {'name': self.name, 'hand': [{'rank': 'Hidden', 'suit': 'Hidden'}] + [c.to_dict() for c in self.hand[1:]], 'value': '?', 'stand': self.stand, 'bust': self.bust, 'is_bot': self.is_bot}
        return {'name': self.name, 'hand': [c.to_dict() for c in self.hand], 'value': self.hand_value(), 'stand': self.stand, 'bust': self.bust, 'is_bot': self.is_bot}

class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.players: Dict[str, Player] = {}
        self.dealer = Player('Dealer')
        self.deck: List[Card] = []
        self.turn_order: List[str] = []
        self.current_turn = 0
        self.started = False
    def reset(self):
        self.deck = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.deck)
        for p in self.players.values():
            p.hand = []
            p.stand = False
            p.bust = False
        self.dealer.hand = []
        self.dealer.stand = False
        self.dealer.bust = False
        self.turn_order = list(self.players.keys())
        self.current_turn = 0
        self.started = False
    def deal_initial(self):
        for _ in range(2):
            for p in self.players.values():
                p.hand.append(self.deck.pop())
            self.dealer.hand.append(self.deck.pop())
        self.started = True
    def add_bot(self):
        bot_num = 1
        while f"Bot{bot_num}" in self.players:
            bot_num += 1
        bot_name = f"Bot{bot_num}"
        self.players[bot_name] = Player(bot_name, is_bot=True)
        self.turn_order.append(bot_name)
        return bot_name
    def to_dict(self):
        return {
            'players': [p.to_dict() for p in self.players.values()],
            'dealer': self.dealer.to_dict(hide_first_card=not self.is_over()),
            'turn': self.turn_order[self.current_turn] if self.started and not self.is_over() else None,
            'started': self.started,
            'over': self.is_over(),
        }
    def is_over(self):
        # Game is over if all players have stood or busted
        return self.started and all(p.stand or p.bust for p in self.players.values())
    def next_turn(self):
        while self.current_turn < len(self.turn_order) - 1:
            self.current_turn += 1
            pname = self.turn_order[self.current_turn]
            if not (self.players[pname].stand or self.players[pname].bust):
                return
        # All players done, dealer plays
        self.dealer_play()
    def dealer_play(self):
        while self.dealer.hand_value() < 17:
            self.dealer.hand.append(self.deck.pop())
        if self.dealer.hand_value() > 21:
            self.dealer.bust = True
        self.dealer.stand = True

rooms: Dict[str, Room] = {}
connections: Dict[str, List[WebSocket]] = {}

async def broadcast(room_id: str, data: Any):
    for ws in connections.get(room_id, []):
        await ws.send_json(data)

@app.websocket("/ws/{room_id}/{player_name}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, player_name: str):
    await websocket.accept()
    if room_id not in rooms:
        rooms[room_id] = Room(room_id)
    if room_id not in connections:
        connections[room_id] = []
    connections[room_id].append(websocket)
    room = rooms[room_id]
    if player_name not in room.players:
        room.players[player_name] = Player(player_name)
    await broadcast(room_id, {"type": "state", "state": room.to_dict()})
    try:
        while True:
            msg = await websocket.receive_json()
            action = msg.get('action')
            if action == 'add_bot':
                bot_name = room.add_bot()
                await broadcast(room_id, {"type": "state", "state": room.to_dict()})
            if action == 'start':
                room.reset()
                room.deal_initial()
                await broadcast(room_id, {"type": "state", "state": room.to_dict()})
            elif action == 'hit':
                player = room.players[player_name]
                if not (player.stand or player.bust) and room.turn_order[room.current_turn] == player_name:
                    player.hand.append(room.deck.pop())
                    if player.hand_value() > 21:
                        player.bust = True
                        player.stand = True
                    await broadcast(room_id, {"type": "state", "state": room.to_dict()})
            elif action == 'stand':
                player = room.players[player_name]
                if not player.stand and room.turn_order[room.current_turn] == player_name:
                    player.stand = True
                    await broadcast(room_id, {"type": "state", "state": room.to_dict()})
            # Bot logic: if it's a bot's turn, make its move automatically
            while room.started and not room.is_over() and room.players[room.turn_order[room.current_turn]].is_bot:
                bot = room.players[room.turn_order[room.current_turn]]
                # Simple bot strategy: hit if under 16, else stand
                if bot.hand_value() < 16:
                    bot.hand.append(room.deck.pop())
                    if bot.hand_value() > 21:
                        bot.bust = True
                        bot.stand = True
                else:
                    bot.stand = True
                await broadcast(room_id, {"type": "state", "state": room.to_dict()})
                if bot.stand or bot.bust:
                    room.next_turn()
            # Advance turn if needed
            if room.started and not room.is_over():
                current_player = room.players[room.turn_order[room.current_turn]]
                if current_player.stand or current_player.bust:
                    room.next_turn()
                    await broadcast(room_id, {"type": "state", "state": room.to_dict()})
            # If game over, broadcast final state
            if room.is_over():
                await broadcast(room_id, {"type": "state", "state": room.to_dict()})
    except WebSocketDisconnect:
        connections[room_id].remove(websocket)
        if not connections[room_id]:
            del connections[room_id]
            del rooms[room_id]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 