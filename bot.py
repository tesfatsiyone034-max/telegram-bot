import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# === Start Command ===
def start(update: Update, context: CallbackContext):
    return menu(update, context)

# === Main Menu ===
def menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📚 Textbook", callback_data="textbook")],
        [InlineKeyboardButton("📘 Teacher Guide", callback_data="teacherguide")],
        [InlineKeyboardButton("📝 Entrance Exam", callback_data="entrance")],
        [InlineKeyboardButton("🏛️ Ministry Exam", callback_data="ministry")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("📖 Please choose:", reply_markup=reply_markup)

# === Callback Handler ===
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # Textbook & Teacher Guide
    if query.data == "textbook":
        keyboard = [
            [InlineKeyboardButton("Primary Books", callback_data="primary_textbook")],
            [InlineKeyboardButton("Secondary Books", callback_data="secondary_textbook")],
        ]
        query.edit_message_text("Choose book type:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "teacherguide":
        keyboard = [
            [InlineKeyboardButton("Primary Books", callback_data="primary_tg")],
            [InlineKeyboardButton("Secondary Books", callback_data="secondary_tg")],
        ]
        query.edit_message_text("Choose teacher guide:", reply_markup=InlineKeyboardMarkup(keyboard))

    # Primary Placeholder
    elif query.data in ["primary_textbook", "primary_tg"]:
        query.edit_message_text("📌 Coming soon...")

    # Secondary Textbook
    elif query.data == "secondary_textbook":
        keyboard = [
            [InlineKeyboardButton("Grade 9", url="https://t.me/EthioBookGrade1_12/57?single")],
            [InlineKeyboardButton("Grade 10", url="https://t.me/EthioBookGrade1_12/80?single")],
            [InlineKeyboardButton("Grade 11", url="https://t.me/EthioBookGrade1_12/102?single")],
            [InlineKeyboardButton("Grade 12", callback_data="comingsoon")],
        ]
        query.edit_message_text("📘 Choose a grade:", reply_markup=InlineKeyboardMarkup(keyboard))

    # Secondary Teacher Guide
    elif query.data == "secondary_tg":
        keyboard = [
            [InlineKeyboardButton("Grade 9", url="https://t.me/EthioBookGrade1_12/67")],
            [InlineKeyboardButton("Grade 10", url="https://t.me/EthioBookGrade1_12/91?single")],
            [InlineKeyboardButton("Grade 11", url="https://t.me/EthioBookGrade1_12/113?single")],
            [InlineKeyboardButton("Grade 12", url="https://t.me/EthioBookGrade1_12/123?single")],
        ]
        query.edit_message_text("📘 Choose a grade:", reply_markup=InlineKeyboardMarkup(keyboard))

    # Entrance Exam
    elif query.data == "entrance":
        keyboard = [
            [InlineKeyboardButton("Natural Science", callback_data="entrance_natural")],
            [InlineKeyboardButton("Social Science", callback_data="entrance_social")],
        ]
        query.edit_message_text("📝 Entrance Exam - Choose stream:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "entrance_natural":
        keyboard = [
            [InlineKeyboardButton("Maths", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("English", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("Chemistry", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("Physics", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("Biology", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("Aptitude", url="https://fetena.net/exam/entrance")],
        ]
        query.edit_message_text("📘 Natural Science Subjects:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "entrance_social":
        keyboard = [
            [InlineKeyboardButton("Maths", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("English", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("Civics", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("Geography", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("History", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("Economics", url="https://fetena.net/exam/entrance")],
        ]
        query.edit_message_text("📘 Social Science Subjects:", reply_markup=InlineKeyboardMarkup(keyboard))

    # Ministry Exam
    elif query.data == "ministry":
        keyboard = [
            [InlineKeyboardButton("Maths", url="https://fetena.net/exam/ministry")],
            [InlineKeyboardButton("English", url="https://fetena.net/exam/ministry")],
            [InlineKeyboardButton("General Science", url="https://fetena.net/exam/ministry")],
            [InlineKeyboardButton("Citizenship", url="https://fetena.net/exam/ministry")],
            [InlineKeyboardButton("Social Study", url="https://fetena.net/exam/ministry")],
        ]
        query.edit_message_text("🏛️ Ministry Exam Subjects:", reply_markup=InlineKeyboardMarkup(keyboard))

    # Coming soon
    elif query.data == "comingsoon":
        query.edit_message_text("📌 Coming soon...")

# === Main Function ===
def main():
    import os
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Set in Render Environment Variables
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()