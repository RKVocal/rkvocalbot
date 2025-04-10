from flask import Flask
import os
import asyncio
from threading import Thread

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

app = Flask(__name__)

# Конфигурация
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHANNEL_ID = -1002673799333

WELCOME_MESSAGE = """
🎤 *Здравствуйте!* Я помощник *RKVocal*.

🎧 Отправьте мне *пример своего вокала* — это может быть *аудио* или *видео* файл.

📩 Жду ваш материал!
"""

THANK_YOU_MESSAGE = """
✅ *Спасибо!*

💡 Возможно, *именно ваш вокал* будет разобран в следующих видео *RKVocal*. 🎬
"""

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("🎥 YouTube", url="https://www.youtube.com/@rkvocal")],
    [InlineKeyboardButton("✈️ Telegram", url="https://t.me/rk_vocal")]
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode="Markdown")

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(THANK_YOU_MESSAGE, parse_mode="Markdown", reply_markup=keyboard)
    await update.message.forward(chat_id=CHANNEL_ID)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚠️ Бот принимает *только аудио и видео файлы*.",
        parse_mode="Markdown"
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f'Ошибка: {context.error}')

@app.route('/')
def home():
    return "🤖 Бот RKVocal работает!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

async def run_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.AUDIO | filters.VIDEO | filters.VOICE | filters.Document.ALL,
        handle_media
    ))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text
    ))
    application.add_error_handler(error_handler)

    # Вручную инициализируем и запускаем бота (без .run_polling())
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("🤖 Бот запущен...")

if __name__ == '__main__':
    if not TOKEN:
        print("❌ Токен не найден в Secrets!")
    else:
        # Flask запускаем в отдельном потоке
        Thread(target=run_flask).start()

        # Бот — в асинхронной среде
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(run_bot())
            loop.run_forever()
        except Exception as e:
            print(f"❌ Ошибка запуска: {e}")
