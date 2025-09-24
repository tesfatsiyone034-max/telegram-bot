import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

flask_app = Flask(__name__)
app = Application.builder().token(TOKEN).build()

# --- Menu ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Hello 👋", callback_data="hi")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bot is alive ✅", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("You pressed Hello 👋")

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

# --- Webhook Route ---
@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return "ok", 200

# --- Startup (set webhook only once) ---
@app.on_startup
async def on_startup(app_: Application):
    await app_.bot.set_webhook(WEBHOOK_URL)