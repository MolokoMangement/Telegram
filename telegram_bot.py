from flask import Flask, request, jsonify
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

app = Flask(__name__)
TOKEN = "7128626321:AAEiBR9_wCkYBXmNRv0V5gZfxKs7h65cw5c"
bot = Bot(token=TOKEN)
URL = "https://molokomanagement-1ca2f474c16e.herokuapp.com/"

@app.route('/')
def index():
    return 'The bot is running!'

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return jsonify({"status": "ok"})

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
            await query.edit_message_text(text=f"Opening {url}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=url)

def main():
    global dispatcher
    application = Application.builder().token(TOKEN).build()
    dispatcher = application.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Set webhook
    application.run_webhook(listen="0.0.0.0",
                            port=int(os.environ.get('PORT', 5000)),
                            url_path=TOKEN,
                            webhook_url=URL + TOKEN)

if __name__ == '__main__':
    main()
