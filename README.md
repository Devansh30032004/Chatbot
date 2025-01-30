# Telegram AI Chatbot

A Telegram chatbot powered by Google's Gemini API with MongoDB for user management and message storage. The bot supports AI-based chat, image/file analysis, and web search functionalities.

## Features
- **User Registration**: Securely stores user data in MongoDB.
- **AI-Powered Chat**: Uses Gemini API for intelligent responses.
- **File & Image Analysis**: Processes and extracts insights from uploaded files/images.
- **Web Search Integration**: Provides relevant search results for queries.
- **MongoDB Storage**: Stores user chats and uploaded files efficiently.

## Tech Stack
- **Python** (Main Bot Logic)
- **MongoDB** (Database for user & chat storage)
- **Telegram Bot API** (For bot communication)
- **Gemini API** (AI-based chat functionality)

## Setup & Installation

### Prerequisites
- Python 3.8+
- MongoDB Atlas account
- Telegram Bot Token
- Gemini API Key

### Installation Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/Devansh30032004/TelegramAIChatbot.git
   cd TelegramAIChatbot
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Configure Environment Variables:
   Create a `.env` file and add:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   GEMINI_API_KEY=your_gemini_api_key
   MONGO_URI=mongodb+srv://your_username:your_password@cluster0.mongodb.net/telegram_bot?retryWrites=true&w=majority&tls=true
   ```

4. Run the bot:
   ```sh
   python bot.py
   ```

## MongoDB Schema

### Users Collection
```json
{
  "user_id": 123456789,
  "username": "devansh",
  "registered_at": "2025-01-29T12:00:00Z"
}
```

### Chats Collection
```json
{
  "user_id": 123456789,
  "message": "Hello, bot!",
  "response": "Hi there! How can I help you?",
  "timestamp": "2025-01-29T12:05:00Z"
}
```

## Troubleshooting
- **MongoDB Connection Error**: Ensure your URI contains a database name (`telegram_bot`).
- **TLS/SSL Issues**: Try adding `tlsAllowInvalidCertificates=True` in your MongoClient setup.

## License
This project is licensed under the MIT License.

## Contact
For any queries, reach out to [Devansh Srivastava](https://github.com/Devansh30032004).
