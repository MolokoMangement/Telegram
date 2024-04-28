from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import os
import threading

app = Flask(__name__)  # Create a Flask app

@app.route('/')
def index():
    return 'The bot is running!'  # Simple route to show the bot is running

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Покажите мне как (на русском)🇷🇺", callback_data='1')],
                [InlineKeyboardButton("Покажіть мені як (українською) 🇺🇦", callback_data='2')],
                [InlineKeyboardButton("Поговорите с живым человеком 😀", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Я готов трансформировать свою жизнь 🚀:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    selected_option = query.data
    urls = {
        '1': 'https://pitch.com/v/pd-in-russian-imrthj',
        '2': 'https://pitch.com/v/pd-in-ukrainian-nvkuc9',
        '3': 'https://t.me/DavidBeaumont'
    }

    url = urls.get(selected_option)

    if url:
        if selected_option == '3':
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Opening {url} in another chat.")
            await context.bot.send_message(chat_id='@DavidBeaumont', text="Hello from the bot!")
        else:
            await query.message.reply_text(f"Opening {url}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=url)

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)

def run_bot():
    application = Application.builder().token("7128626321:AAEiBR9_wCkYBXmNRv0V5gZfxKs7h65cw5c").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

if __name__ == '__main__':
    # Run Flask and Telegram bot in separate threads
    threading.Thread(target=run_flask).start()
    threading.Thread(target=run_bot).start()

