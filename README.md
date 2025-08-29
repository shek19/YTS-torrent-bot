# 🎬 YTS Telegram Bot

A Telegram bot that searches for movies on YTS (YIFY) and downloads torrent files directly to users, bypassing geo-restrictions and providing a seamless movie torrenting experience.

## ✨ Features

- 🔍 **Movie Search**: Search for movies by title and year
- 📁 **Direct File Download**: Downloads and sends actual `.torrent` files via Telegram
- 🌍 **Geo-blocking Bypass**: Downloads happen on server, avoiding regional restrictions
- 📱 **User-Friendly Interface**: Simple commands with progress updates
- 🔄 **Fallback System**: Provides direct download links if file download fails
- 🚀 **Fast & Reliable**: Built with FastAPI and modern async/await patterns
- 🔧 **Production Ready**: Webhook support for deployment on platforms like Render, Heroku, etc.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shek19/YTS-torrent-bot.git
   cd YTS-torrent-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create configuration file**
   ```bash
   cp config.py.example config.py
   ```

4. **Add your bot token**
   ```python
   # config.py
   TELEGRAM_BOT_TOKEN = "your_bot_token_here"
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## 📱 Bot Commands

- `/start` - Welcome message and instructions
- `/movie <movie_name>` - Search for a movie
  - Example: `/movie Inception`
  - Example: `/movie The Dark Knight 2008`

## 🏗️ Project Structure

```
yts-telegram-bot/
├── main.py              # FastAPI application entry point
├── bot.py               # Telegram bot handlers and logic
├── config.py            # Configuration settings
├── utils/
│   └── yts_api.py       # YTS API integration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables

For production deployments, you can use environment variables:

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export RENDER_EXTERNAL_URL="https://your-app.onrender.com"  # For webhook mode
```

### Webhook vs Polling

The bot supports both webhook and polling modes:

**Webhook Mode (Recommended for production):**
- Automatically enabled when `RENDER_EXTERNAL_URL` is set
- More efficient and reliable for cloud deployments
- Used in the main branch

**Polling Mode:**
- Suitable for development and local testing
- Check the `polling-mode` branch for implementation

## 🚀 Deployment

### Deploy to Render

1. **Fork this repository**

2. **Create a new Web Service on Render**
   - Connect your GitHub repository
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   - `TELEGRAM_BOT_TOKEN`: Your bot token from BotFather
   - `RENDER_EXTERNAL_URL`: Your render app URL (e.g., `https://your-app.onrender.com`)

4. **Deploy**
   - Render will automatically deploy your bot
   - The bot will be accessible via webhook

### Deploy to Heroku

1. **Install Heroku CLI and login**
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**
   ```bash
   heroku create your-bot-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=your_bot_token
   heroku config:set RENDER_EXTERNAL_URL=https://your-bot-name.herokuapp.com
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Local Development

For local development with polling mode:

```bash
# Use the polling branch
git checkout polling-mode

# Run locally
uvicorn main:app --reload or python -m fastapi dev
```

## 📋 Requirements

```txt
fastapi
uvicorn
python-telegram-bot
requests
aiohttp
```

## 🔍 How It Works

1. **User sends a movie search request** via `/movie <movie_name>` --note: the movie name must be accurate, search google for movie name, you can also add year to be exact
2. **Bot queries YTS API** to find matching movies
3. **Bot retrieves torrent information** including download URLs
4. **Server downloads .torrent files** to temporary storage
5. **Bot sends files directly to user** via Telegram
6. **Temporary files are cleaned up** after sending
7. **Fallback system provides direct links** if file download fails

## 🛡️ Features & Benefits

### Bypasses Geo-restrictions
- Downloads happen on your server, not user's location
- Users in restricted regions can access YTS content

### Better User Experience
- No need to visit external websites
- Direct file delivery via Telegram
- Works with any torrent client

### Privacy Focused
- No user data storage
- Temporary files are automatically deleted
- Server-side processing protects user IP

## 🚨 Important Notes

### Legal Disclaimer
This bot is for educational purposes only. Users are responsible for complying with their local laws regarding torrenting and copyright. The developers do not condone piracy or copyright infringement.

### Rate Limiting
- The bot limits to 3 torrent files per request to avoid spam
- YTS API has its own rate limiting

### File Size Limits
- Telegram has a 50MB limit for bot file uploads
- Most .torrent files are well under this limit

## 🛠️ Development

### Adding New Features

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Code Structure

- `main.py`: FastAPI app with webhook handling
- `bot.py`: Telegram bot logic and command handlers
- `utils/yts_api.py`: YTS API integration
- `config.py`: Configuration management

## 🐛 Troubleshooting

### Common Issues

**Bot not responding:**
- Check if bot token is correct
- Ensure webhook URL is properly set
- Check server logs for errors

**Torrent downloads failing:**
- YTS might be temporarily unavailable
- Geo-blocking might affect server location
- Check internet connectivity

**Files not sending:**
- Check file size (Telegram 50MB limit)
- Verify file permissions
- Check disk space on server


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 🙏 Acknowledgments

- [YTS/YIFY](https://yts.mx/) for providing the movie torrent API
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the excellent Telegram bot library
- [FastAPI](https://fastapi.tiangolo.com/) for the modern web framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/shek19/YTS-torrent-bot/issues) page
2. Create a new issue with detailed information

---

⭐ If you found this project helpful, please give it a star on GitHub!

## 🔄 Recent Updates

- ✅ Added webhook support for production deployment
- ✅ Implemented torrent file downloading and sending
- ✅ Enhanced geo-blocking bypass capabilities
