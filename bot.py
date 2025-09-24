import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Bot Token & Webhook URL ---
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# --- Flask app ---
flask_app = Flask(__name__)

# --- Telegram Application ---
app = Application.builder().token(TOKEN).build()

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Hello 👋", callback_data="hi")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bot is alive ✅", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("You pressed Hello 👋")

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

# --- Webhook route ---
@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return "ok", 200

# --- Set webhook on startup ---
@app.before_serving
async def set_webhook():
    await app.bot.set_webhook(WEBHOOK_URL)