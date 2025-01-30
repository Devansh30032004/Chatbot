
import os
import logging
import telebot
import google.generativeai as genai
import pymongo
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timezone
from googleapiclient.discovery import build

# Load environment variables
TELEGRAM_TOKEN = "7891949863:AAHdJTm2QVejqbefRA-WV3hPgLg7Ofzn-tU"
GEMINI_API_KEY = "AIzaSyA2aqrT1FFYlTHKSOKB51LgSNsOG8oaW-A"
MONGO_URI = "mongodb+srv://prdevansh2155:Devansh#1234@cluster0.1c8pg.mongodb.net/telegram_bot?retryWrites=true&w=majority&appName=Cluster0&tls=true"
GOOGLE_CSE_KEY = "AIzaSyDjL8HPrYOD6LbdZ4BaV2Du6CRGbhdyK5M"
GOOGLE_CSE_ID = "939a85aeab5a9407d"

# Initialize services
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key = GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

mongo_client = pymongo.MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db = mongo_client["telegram_bot"]
users_collection = db["users"]
chats_collection = db["chats"]
files_collection = db["files"]

# Enable logging
logging.basicConfig(level=logging.INFO)

def register_user(message):
    user_data = {
        "chat_id": message.chat.id,
        "first_name": message.from_user.first_name,
        "username": message.from_user.username,
        "phone_number": None,
        "registered_at": datetime.now(timezone.utc)
    }
    users_collection.update_one({"chat_id": message.chat.id}, {"$set": user_data}, upsert=True)
    bot.send_message(message.chat.id, "Please share your phone number.", reply_markup=get_phone_keyboard())

def get_phone_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("Share Contact", request_contact=True)
    keyboard.add(button)
    return keyboard

@bot.message_handler(content_types=['contact'])
def save_phone_number(message):
    users_collection.update_one({"chat_id": message.chat.id}, {"$set": {"phone_number": message.contact.phone_number}})
    bot.send_message(message.chat.id, "Registration complete! You can now start chatting.")

@bot.message_handler(commands=['start'])
def start(message):
    if not users_collection.find_one({"chat_id": message.chat.id}):
        register_user(message)
    else:
        bot.send_message(message.chat.id, "Welcome back! How can I assist you?")

@bot.message_handler(func=lambda message: True)
def chat_with_gemini(message):
    try:
        chat_entry = {
            "chat_id": message.chat.id,
            "user_input": message.text,
            "timestamp": datetime.now(timezone.utc)
        }
        
        response = model.generate_content(message.text)  # Corrected method call
        bot.send_message(message.chat.id, response.text)

        chat_entry["bot_response"] = response.text
        chats_collection.insert_one(chat_entry)
    except Exception as e:
        bot.send_message(message.chat.id, "Sorry, an error occurred while processing your request.")
        logging.error(f"Error in chat_with_gemini: {e}")

@bot.message_handler(content_types=['photo', 'document'])
def handle_files(message):
    try:
        file_id = message.photo[-1].file_id if message.photo else message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        os.makedirs("downloads", exist_ok=True)
        file_path = f"downloads/{file_info.file_path.split('/')[-1]}"
        with open(file_path, "wb") as f:
            f.write(downloaded_file)

        description_prompt = "Describe this image."
        description = model.generate_content(description_prompt).text  # Fixed API call

        bot.send_message(message.chat.id, f"Analysis: {description}")

        files_collection.insert_one({
            "chat_id": message.chat.id,
            "filename": file_info.file_path,
            "description": description
        })
    except Exception as e:
        bot.send_message(message.chat.id, "Sorry, an error occurred while processing your file.")
        logging.error(f"Error in handle_files: {e}")

@bot.message_handler(commands=['websearch'])
def web_search(message):
    bot.send_message(message.chat.id, "Send your query for web search.")
    bot.register_next_step_handler(message, search_query)

def search_query(message):
    try:
        query = message.text
        search_results = perform_web_search(query)
        response = f"Top Results for '{query}':\n" + "\n".join(search_results)
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, "Sorry, an error occurred while performing the web search.")
        logging.error(f"Error in search_query: {e}")

def perform_web_search(query):
    try:
        search_engine = build("customsearch", "v1", developerKey=GOOGLE_CSE_KEY)
        results = search_engine.cse().list(q=query, cx=GOOGLE_CSE_ID).execute()
        return [f"{item['title']}: {item['link']}" for item in results.get("items", [])]
    except Exception as e:
        logging.error(f"Error in perform_web_search: {e}")
        return ["No results found."]

if __name__ == "__main__":
    logging.info("Bot is running...")
    bot.polling(non_stop=True)

try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client.get_database()
    print("Connected successfully to MongoDB")
except Exception as e:
    print(f"Connection error: {e}")