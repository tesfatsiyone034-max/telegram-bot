from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import os

# Get token from environment variable (Fly.io or local)
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# --- Handlers ---
def start(update: Update, context: CallbackContext):
    return menu(update, context)

def menu(update: Update, context: CallbackContext):
    main_menu = [
        ["📘 Textbook", "👨‍🏫 Teacher Guide"],
        ["📄 Entrance Exam", "🏛️ Ministry Exam"]
    ]
    reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    update.message.reply_text("👋 Welcome! Choose an option:", reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    # === TEXTBOOK ===
    if text == "📘 Textbook":
        submenu = [["📚 Primary Books", "📖 Secondary Books"], ["🔙 Back to Menu"]]
        reply_markup = ReplyKeyboardMarkup(submenu, resize_keyboard=True)
        update.message.reply_text("Choose textbook type:", reply_markup=reply_markup)

    elif text == "📚 Primary Books":
        update.message.reply_text("📚 Coming soon!")

    elif text == "📖 Secondary Books":
        submenu = [["Grade 9", "Grade 10"], ["Grade 11", "Grade 12"], ["🔙 Back to Menu"]]
        reply_markup = ReplyKeyboardMarkup(submenu, resize_keyboard=True)
        update.message.reply_text("Choose grade:", reply_markup=reply_markup)

    elif text == "Grade 9":
        update.message.reply_text("📖 Opening Grade 9 book...")
        update.message.reply_text("https://t.me/EthioBookGrade1_12/57?single")

    elif text == "Grade 10":
        update.message.reply_text("📖 Opening Grade 10 book...")
        update.message.reply_text("https://t.me/EthioBookGrade1_12/80?single")

    elif text == "Grade 11":
        update.message.reply_text("📖 Opening Grade 11 book...")
        update.message.reply_text("https://t.me/EthioBookGrade1_12/102?single")

    elif text == "Grade 12":
        update.message.reply_text("📚 Coming soon!")

    # === TEACHER GUIDE ===
    elif text == "👨‍🏫 Teacher Guide":
        submenu = [["TG Grade 9", "TG Grade 10"], ["TG Grade 11", "TG Grade 12"], ["🔙 Back to Menu"]]
        reply_markup = ReplyKeyboardMarkup(submenu, resize_keyboard=True)
        update.message.reply_text("Choose teacher guide:", reply_markup=reply_markup)

    elif text == "TG Grade 9":
        update.message.reply_text("👨‍🏫 Opening Teacher Guide Grade 9...")
        update.message.reply_text("https://t.me/EthioBookGrade1_12/67")

    elif text == "TG Grade 10":
        update.message.reply_text("👨‍🏫 Opening Teacher Guide Grade 10...")
        update.message.reply_text("https://t.me/EthioBookGrade1_12/91?single")

    elif text == "TG Grade 11":
        update.message.reply_text("👨‍🏫 Opening Teacher Guide Grade 11...")
        update.message.reply_text("https://t.me/EthioBookGrade1_12/113?single")

    elif text == "TG Grade 12":
        update.message.reply_text("👨‍🏫 Opening Teacher Guide Grade 12...")
        update.message.reply_text("https://t.me/EthioBookGrade1_12/123?single")

    # === ENTRANCE EXAM ===
    elif text == "📄 Entrance Exam":
        submenu = [["Natural Science", "Social Science"], ["🔙 Back to Menu"]]
        reply_markup = ReplyKeyboardMarkup(submenu, resize_keyboard=True)
        update.message.reply_text("Choose stream:", reply_markup=reply_markup)

    elif text == "Natural Science":
        subjects = [["Maths", "English"], ["Chemistry", "Physics", "Biology"], ["Aptitude"], ["🔙 Back to Menu"]]
        reply_markup = ReplyKeyboardMarkup(subjects, resize_keyboard=True)
        update.message.reply_text("Choose subject:", reply_markup=reply_markup)

    elif text == "Social Science":
        subjects = [["Maths", "English", "Civics"], ["Geography", "History", "Economics"], ["Aptitude"], ["🔙 Back to Menu"]]
        reply_markup = ReplyKeyboardMarkup(subjects, resize_keyboard=True)
        update.message.reply_text("Choose subject:", reply_markup=reply_markup)

    elif text in ["Maths", "English", "Chemistry", "Physics", "Biology", "Civics", "Geography", "History", "Economics", "Aptitude"]:
        update.message.reply_text("📄 Opening Entrance Exam...")
        update.message.reply_text("https://fetena.net/exam/entrance")

    # === MINISTRY EXAM ===
    elif text == "🏛️ Ministry Exam":
        subjects = [["Maths", "English"], ["General Science", "Citizenship"], ["Social Study"], ["🔙 Back to Menu"]]
        reply_markup = ReplyKeyboardMarkup(subjects, resize_keyboard=True)
        update.message.reply_text("Choose subject:", reply_markup=reply_markup)

    elif text in ["General Science", "Citizenship", "Social Study"]:
        update.message.reply_text("📘 Opening Ministry Exam...")
        update.message.reply_text("https://fetena.net/exam/ministry")

    elif text in ["Maths", "English"]:
        update.message.reply_text("📘 Opening Ministry Exam...")
        update.message.reply_text("https://fetena.net/exam/ministry")

    # === BACK TO MENU ===
    elif text == "🔙 Back to Menu":
        return menu(update, context)

    else:
        update.message.reply_text("❌ Unknown option. Use /start to return to menu.")

# --- Main ---
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("✅ Bot started...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()