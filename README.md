# 🃏 Multiplayer Blackjack Web App

A real-time, multiplayer Blackjack game built with **FastAPI** (Python backend) and **vanilla JavaScript** (frontend). Play with friends or challenge AI bots in this beautifully designed web-based card game!

![Blackjack Game](https://img.shields.io/badge/Game-Blackjack-4CAF50?style=for-the-badge&logo=game-controller)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green?style=for-the-badge&logo=fastapi)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-orange?style=for-the-badge&logo=websocket)

## 🎮 Game Features

### Core Gameplay
- **Real-time multiplayer** - Play with friends in the same room
- **AI Bots** - Add computer players to fill empty seats
- **Standard Blackjack rules** - Classic 21 gameplay
- **Live game state** - Real-time updates for all players
- **Turn-based gameplay** - Clear turn indicators and action buttons

### User Experience
- **Beautiful UI** - Modern, responsive design with card animations
- **Emoji avatars** - Unique avatars for each player
- **Fun facts** - Educational Blackjack trivia
- **Confetti celebration** - Visual feedback for winners
- **Mobile-friendly** - Works on desktop and mobile devices

### Technical Features
- **WebSocket communication** - Real-time bidirectional messaging
- **Room-based gameplay** - Join specific game rooms
- **Persistent user data** - Track wins and losses
- **Cross-platform** - Works on Windows, Mac, and Linux

## 🎯 How to Play Blackjack

### Objective
Get as close to 21 as possible without going over. Beat the dealer's hand to win!

### Card Values
- **Number cards (2-10)**: Face value
- **Face cards (J, Q, K)**: 10 points each
- **Aces**: 1 or 11 points (automatically optimized)

### Game Rules
1. **Dealing**: Each player and dealer gets 2 cards initially
2. **Player turns**: Hit (take another card) or Stand (keep current hand)
3. **Dealer rules**: Must hit until reaching 17 or higher
4. **Winning**: Beat dealer's total without busting (going over 21)
5. **Bust**: Going over 21 means automatic loss

### Winning Conditions
- **Player wins**: Higher total than dealer (without busting)
- **Dealer wins**: Player busts OR dealer has higher total
- **Push (Tie)**: Same total as dealer (no win/loss)

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+** installed on your system
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Git** (for cloning the repository)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/blackjack_web.git
   cd blackjack_web
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Start the server**
   ```bash
   python main.py
   ```
   The server will start on `http://localhost:8000`

4. **Open the frontend**
   - Navigate to `frontend/index.html` in your browser
   - Or use a local server for better experience:
     ```bash
     cd frontend
     python -m http.server 8080
     ```
     Then visit `http://localhost:8080`

## 🎲 How to Play

### Joining a Game
1. **Enter your name** - Choose any username you like
2. **Enter room ID** - Create a new room or join existing one
3. **Click "Join Room"** - Connect to the game server

### Game Setup
1. **Add players** - Invite friends or add AI bots
2. **Start game** - Click "Start Game" when ready
3. **Take turns** - Hit or Stand when it's your turn

### Game Actions
- **Hit** - Take another card (if it's your turn)
- **Stand** - Keep your current hand (if it's your turn)
- **Add Bot** - Add AI player to the game
- **Start Game** - Begin a new round

## 🏗️ Project Structure

```
blackjack_web/
├── backend/
│   ├── main.py              # FastAPI server with game logic
│   ├── requirements.txt     # Python dependencies
│   └── users.json          # User data storage
├── frontend/
│   ├── index.html          # Main game interface
│   ├── app.js             # Game logic and WebSocket handling
│   └── style.css          # Styling and animations
└── README.md              # This file
```

## 🔧 Technical Details

### Backend (FastAPI)
- **WebSocket endpoints** for real-time communication
- **REST API** for user authentication and scoring
- **Game state management** with room-based sessions
- **AI bot logic** with simple hit/stand strategy

### Frontend (Vanilla JavaScript)
- **WebSocket client** for real-time updates
- **Responsive UI** with CSS animations
- **Card rendering** with emoji suits
- **Game state synchronization**

### Key Classes
- **`Card`**: Represents individual playing cards
- **`Player`**: Manages player hands and game state
- **`Room`**: Handles game room logic and turn management
- **`Dealer`**: Special player with automated rules

## 🌐 API Endpoints

### WebSocket
- `ws://localhost:8000/ws/{room_id}/{player_name}` - Game communication

### REST API
- `POST /api/signup` - User registration
- `POST /api/login` - User authentication
- `GET /api/profile` - Get user profile
- `POST /api/score` - Update win/loss statistics

## 🎨 Customization

### Adding New Features
- **New game modes** - Modify `Room` class in `main.py`
- **Enhanced AI** - Improve bot strategy in `dealer_play()`
- **UI themes** - Update colors in `style.css`
- **Sound effects** - Add audio files and JavaScript handlers

### Styling
The game uses a modern dark theme with:
- **Color scheme**: Dark blues and greens
- **Animations**: Card hover effects and confetti
- **Typography**: Clean, readable fonts
- **Responsive design**: Works on all screen sizes

## 🐛 Troubleshooting

### Common Issues

**Server won't start**
- Check Python version: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check port availability: Change port in `main.py`

**WebSocket connection fails**
- Ensure backend is running on `localhost:8000`
- Check browser console for errors
- Try refreshing the page

**Game not updating**
- Check internet connection
- Verify WebSocket connection status
- Restart both frontend and backend

### Debug Mode
Enable debug logging by modifying `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

We welcome contributions! Here's how to help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests (when available)
pytest

# Format code
black backend/

# Lint code
flake8 backend/
```

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **WebSocket** for real-time communication
- **Emoji** for beautiful card representations
- **CSS animations** for smooth user experience

## 📞 Support

If you encounter any issues or have questions:

1. **Check the troubleshooting section** above
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Contact the maintainers** for direct support

---

**Happy gaming! 🎉 May the cards be ever in your favor! 🃏** 
