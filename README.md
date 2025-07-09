# Multiplayer Blackjack Web App

A real-time, multiplayer Blackjack game built with FastAPI (Python) and a modern web frontend.

## Features
- Join a room and play with friends in real time
- FastAPI backend with WebSocket support
- Modern, responsive UI
- Easy to extend with game logic and creative features

## Getting Started

### 1. Backend (FastAPI)
```bash
cd blackjack_web/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend
Just open `blackjack_web/frontend/index.html` in your browser.

**Note:** For local development, you may need to use a simple HTTP server to avoid CORS issues:
```bash
cd blackjack_web/frontend
python -m http.server 8080
```
Then visit [http://localhost:8080](http://localhost:8080)

## Roadmap
- Add full Blackjack game logic and UI
- Real-time updates for all players
- Beautiful card/table graphics
- Room/lobby management

