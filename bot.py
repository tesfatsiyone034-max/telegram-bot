import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from flask import Flask, request

# --- Get Bot Token ---
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-app.onrender.com/webhook

# --- Flask app for webhook ---
flask_app = Flask(__name__)

# --- Links ---
TEXTBOOK_PRIMARY_LINKS = {f"Grade{i}": "https://t.me/EthioBookGrade1_12/comingsoon" for i in range(1, 9)}
TEXTBOOK_SECONDARY_LINKS = {
    "Grade9": "https://t.me/EthioBookGrade1_12/57?single",
    "Grade10": "https://t.me/EthioBookGrade1_12/80?single",
    "Grade11": "https://t.me/EthioBookGrade1_12/102?single",
    "Grade12": "https://t.me/EthioBookGrade1_12/comingsoon"
}
TEACHERGUIDE_PRIMARY_LINKS = {f"Grade{i}": "https://t.me/EthioBookGrade1_12/comingsoon" for i in range(1, 9)}
TEACHERGUIDE_SECONDARY_LINKS = {
    "Grade9": "https://t.me/EthioBookGrade1_12/67",
    "Grade10": "https://t.me/EthioBookGrade1_12/91?single",
    "Grade11": "https://t.me/EthioBookGrade1_12/113?single",
    "Grade12": "https://t.me/EthioBookGrade1_12/123?single"
}

ENTRANCE_LINK = "https://fetena.net/exam/entrance"
ENTRANCE_NS_SUBJECTS = ["Maths", "English", "Chemistry", "Physics", "Biology", "Aptitude"]
ENTRANCE_SS_SUBJECTS = ["Maths", "English", "Civics", "Geography", "History", "Economics"]

MINISTRY_LINK = "https://fetena.net/exam/ministry"
MINISTRY_SUBJECTS = ["Maths", "English", "General Science", "Citizenship", "Social Study"]

# --- Helper function to generate grade buttons ---
def grade_buttons(links_dict):
    buttons = [[InlineKeyboardButton(grade, url=url)] for grade, url in links_dict.items()]
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")])
    return buttons

# --- Menu ---
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 Textbook", callback_data="textbook")],
        [InlineKeyboardButton("🧑‍🏫 Teacher Guide", callback_data="teacherguide")],
        [InlineKeyboardButton("📄 Entrance Exam", callback_data="entrance")],
        [InlineKeyboardButton("🏛️ Ministry Exam", callback_data="ministry")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("👋 Please choose an option:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text("👋 Please choose an option:", reply_markup=reply_markup)

# --- Start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await menu(update, context)

# --- Button Handler ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_to_menu":
        await menu(update, context)
        return

    if data == "textbook":
        keyboard = [
            [InlineKeyboardButton("📚 Primary (1–8)", callback_data="textbook_primary")],
            [InlineKeyboardButton("🎓 Secondary (9–12)", callback_data="textbook_secondary")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
        ]
        await query.edit_message_text("📘 Choose books:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "textbook_primary":
        await query.edit_message_text("📚 Select grade:", reply_markup=InlineKeyboardMarkup(grade_buttons(TEXTBOOK_PRIMARY_LINKS)))

    elif data == "textbook_secondary":
        await query.edit_message_text("🎓 Select grade:", reply_markup=InlineKeyboardMarkup(grade_buttons(TEXTBOOK_SECONDARY_LINKS)))

    elif data == "teacherguide":
        keyboard = [
            [InlineKeyboardButton("📚 Primary (1–8)", callback_data="teacherguide_primary")],
            [InlineKeyboardButton("🎓 Secondary (9–12)", callback_data="teacherguide_secondary")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
        ]
        await query.edit_message_text("🧑‍🏫 Choose guides:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "teacherguide_primary":
        await query.edit_message_text("📚 Select grade:", reply_markup=InlineKeyboardMarkup(grade_buttons(TEACHERGUIDE_PRIMARY_LINKS)))

    elif data == "teacherguide_secondary":
        await query.edit_message_text("🎓 Select grade:", reply_markup=InlineKeyboardMarkup(grade_buttons(TEACHERGUIDE_SECONDARY_LINKS)))

    elif data == "entrance":
        keyboard = [
            [InlineKeyboardButton("🧪 Natural Science", callback_data="entrance_ns")],
            [InlineKeyboardButton("🌍 Social Science", callback_data="entrance_ss")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
        ]
        await query.edit_message_text("📄 Choose exam category:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "entrance_ns":
        keyboard = [[InlineKeyboardButton(subj, url=ENTRANCE_LINK)] for subj in ENTRANCE_NS_SUBJECTS]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="entrance")])
        await query.edit_message_text("🧪 Natural Science:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "entrance_ss":
        keyboard = [[InlineKeyboardButton(subj, url=ENTRANCE_LINK)] for subj in ENTRANCE_SS_SUBJECTS]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="entrance")])
        await query.edit_message_text("🌍 Social Science:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "ministry":
        keyboard = [[InlineKeyboardButton(subj, url=MINISTRY_LINK)] for subj in MINISTRY_SUBJECTS]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")])
        await query.edit_message_text("🏛 Ministry Exam:", reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        await query.edit_message_text("❌ Invalid option", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]]))

# --- Telegram Application ---
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CallbackQueryHandler(button_handler))

# --- Webhook Endpoint ---
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app.bot)
    app.update_queue.put_nowait(update)
    return "ok", 200

# --- Start Flask Server and Set Webhook ---
if __name__ == "__main__":
    import asyncio

    # Set webhook once at startup
    async def set_webhook():
        await app.bot.set_webhook(WEBHOOK_URL)

    asyncio.get_event_loop().run_until_complete(set_webhook())

    port = int(os.getenv("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)