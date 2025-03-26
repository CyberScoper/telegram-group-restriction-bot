
# 🤖 Telegram Bot for User Restriction and Welcome Messaging

This project is a Telegram bot designed to enhance group management by monitoring new members, applying temporary restrictions, and sending welcome messages after the restriction period.

## ✨ Features

- 🕵️ **New Member Detection**: Automatically detects when new members join the group.
- ⏳ **Temporary Restriction**: Restricts new members from sending messages for 12 hours after a waiting period of 7 minutes.
- 👋 **Welcome Message**: Sends a personalized welcome message mentioning the user after the 12-hour restriction period ends, provided the user is still in the group.
- 📝 **Logging**: Includes detailed logging for monitoring bot actions and debugging.

## 🛠 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/CyberScoper/telegram-group-restriction-bot.git
   cd telegram-group-restriction-bot
   ```

2. **Set up Python environment**:
   Ensure you have Python 3.7+ installed.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Add your Telegram bot token**:
   Replace the placeholder token in `main.py`:
   ```python
   application = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
   ```

4. **Run the bot**:
   ```bash
   python main.py
   ```

## 🚀 Usage

- **Start Command**: `/start` – Initializes the bot and confirms it is running.
- **New Member Handling**: The bot automatically tracks new members and starts the restriction process.

## ⚙️ Configuration

- **Delay and Restriction Time**: The waiting time before restriction is 7 minutes, and the restriction duration is 12 hours.
- **Welcome Message Customization**: The message text can be modified in the `schedule_welcome_message` function.

## 🛡 Logging and Debugging

Logs are set up to provide detailed output. You can change the logging level by adjusting:
```python
logging.basicConfig(level=logging.INFO)  # Use DEBUG for more detailed logs
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/telegram-restriction-bot/issues).

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
