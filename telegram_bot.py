from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, Dispatcher
import os

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
HEROKU_URL = "https://molokomanagement-1ca2f474c16e.herokuapp.com/webhook"  # Ensure this matches your Heroku URL

bot = Bot(TOKEN)

def setup_dispatcher():
    dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    return dispatcher

dispatcher = setup_dispatcher()

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok', 200

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Покажите мне как (на русском)🇷🇺", callback_data='1')],
        [InlineKeyboardButton("Покажіть мені як (українською) 🇺🇦", callback_data='2')],
        [InlineKeyboardButton("Поговорите с живым человеком 😀", callback_data='3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Я готов трансформировать свою жизнь 🚀:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await context.bot.send_message(chat_id=update.effective_chat.id, text=url)

if __name__ == '__main__':
    bot.set_webhook(HEROKU_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

