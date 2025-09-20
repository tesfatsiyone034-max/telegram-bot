import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ✅ Use environment variable for token
TOKEN = os.getenv("BOT_TOKEN")

# 🔹 Links for Textbook and Teacher Guide (replace with your real links)
TEXTBOOK_LINKS = {f"Grade{i}": f"https://t.me/c/3087996750/{i+2}" for i in range(1, 13)}
TEACHERGUIDE_LINKS = {f"Grade{i}": f"https://t.me/c/3087996750/{i+20}" for i in range(1, 13)}

# 🔹 Worksheet & Practicing Questions group link
WORKSHEET_GROUP = "https://t.me/YourGroupLinkHere"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 Textbook", callback_data="textbook")],
        [InlineKeyboardButton("🧑‍🏫 Teacher Guide", callback_data="teacherguide")],
        [InlineKeyboardButton("📄 Worksheet & Practicing Questions", callback_data="worksheet")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome! Please choose an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Step 1: Main menu → show grades for Textbook or Teacher Guide
    if query.data == "textbook":
        grade_buttons = [[InlineKeyboardButton(f"Grade {i}", callback_data=f"textbook_Grade{i}")] for i in range(1, 13)]
        reply_markup = InlineKeyboardMarkup(grade_buttons)
        await query.edit_message_text("📚 Select your grade:", reply_markup=reply_markup)

    elif query.data == "teacherguide":
        grade_buttons = [[InlineKeyboardButton(f"Grade {i}", callback_data=f"teacherguide_Grade{i}")] for i in range(1, 13)]
        reply_markup = InlineKeyboardMarkup(grade_buttons)
        await query.edit_message_text("📖 Select your grade:", reply_markup=reply_markup)

    # Step 2: Worksheet → direct group link
    elif query.data == "worksheet":
        await query.edit_message_text(f"📄 Join the Worksheet & Practicing Questions group:\n{WORKSHEET_GROUP}")

    # Step 3: Textbook grade → send link
    elif query.data.startswith("textbook_"):
        grade = query.data.split("_")[1]
        link = TEXTBOOK_LINKS.get(grade, "https://t.me/")
        await query.edit_message_text(f"📘 Textbook for {grade}:\n{link}")

    # Step 4: Teacher Guide grade → send link
    elif query.data.startswith("teacherguide_"):
        grade = query.data.split("_")[1]
        link = TEACHERGUIDE_LINKS.get(grade, "https://t.me/")
        await query.edit_message_text(f"🧑‍🏫 Teacher Guide for {grade}:\n{link}")

# 🔹 Build and run the bot
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()