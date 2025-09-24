from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.getenv("BOT_TOKEN")

# Define menu structure
menus = {
    "main": [
        ["📘 Textbook", "🧑‍🏫 Teacher Guide"],
        ["📄 Entrance Exam", "🏛️ Ministry Exam"]
    ],
    "Textbook": [
        ["📚 Primary Books", "📖 Secondary Books"],
        ["🔙 Back to Menu"]
    ],
    "Secondary Books": [
        ["Grade 9", "Grade 10"],
        ["Grade 11", "Grade 12"],
        ["🔙 Back to Menu"]
    ]
}

# Links for books
book_links = {
    "Grade 9": "https://t.me/EthioBookGrade1_12/57?single",
    "Grade 10": "https://t.me/EthioBookGrade1_12/80?single",
    "Grade 11": "https://t.me/EthioBookGrade1_12/102?single",
    "Grade 12": "Coming soon!"
}

# Track user's current menu
user_menu_state = {}

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_menu_state[chat_id] = "main"
    reply_markup = ReplyKeyboardMarkup(menus["main"], resize_keyboard=True)
    update.message.reply_text("👋 Welcome! Please choose an option:", reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    current_menu = user_menu_state.get(chat_id, "main")

    if text == "🔙 Back to Menu":
        start(update, context)
        return

    # If user selects a submenu
    if text in menus:
        user_menu_state[chat_id] = text
        reply_markup = ReplyKeyboardMarkup(menus[text], resize_keyboard=True)
        update.message.reply_text(f"Choose {text} option:", reply_markup=reply_markup)

    # If user selects a book link
    elif text in book_links:
        update.message.reply_text(f"📖 {text} link:")
        update.message.reply_text(book_links[text])

    else:
        update.message.reply_text("❌ Unknown option. Please use the menu.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("✅ Bot started...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()