from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

TOKEN = "BOT_TOKEN"

# --- Start & Menu ---
def start(update, context):
    main_menu(update)

def menu(update, context):
    main_menu(update)

def main_menu(update):
    keyboard = [
        ["📚 Textbooks", "📘 Teacher Guides"],
        ["📝 Entrance Exam", "🏛 Ministry Exam"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("📖 Welcome!\nChoose an option:", reply_markup=reply_markup)

# --- Handle Textbooks ---
def handle_textbooks(update, context):
    keyboard = [
        [InlineKeyboardButton("📕 Primary Books", callback_data="primary_books")],
        [InlineKeyboardButton("📗 Secondary Books", callback_data="secondary_books")]
    ]
    update.message.reply_text("Choose category:", reply_markup=InlineKeyboardMarkup(keyboard))

def handle_teacher_guides(update, context):
    keyboard = [
        [InlineKeyboardButton("📕 Primary Guides", callback_data="primary_guides")],
        [InlineKeyboardButton("📗 Secondary Guides", callback_data="secondary_guides")]
    ]
    update.message.reply_text("Choose category:", reply_markup=InlineKeyboardMarkup(keyboard))

# --- Entrance Exam ---
def handle_entrance(update, context):
    keyboard = [
        [InlineKeyboardButton("🔬 Natural Science", callback_data="entrance_natural")],
        [InlineKeyboardButton("🌍 Social Science", callback_data="entrance_social")]
    ]
    update.message.reply_text("Choose stream:", reply_markup=InlineKeyboardMarkup(keyboard))

# --- Ministry Exam ---
def handle_ministry(update, context):
    keyboard = [
        [InlineKeyboardButton("📐 Maths", url="https://fetena.net/exam/ministry")],
        [InlineKeyboardButton("📖 English", url="https://fetena.net/exam/ministry")],
        [InlineKeyboardButton("🔬 General Science", url="https://fetena.net/exam/ministry")],
        [InlineKeyboardButton("🧑‍🤝‍🧑 Citizenship", url="https://fetena.net/exam/ministry")],
        [InlineKeyboardButton("🌍 Social Study", url="https://fetena.net/exam/ministry")]
    ]
    update.message.reply_text("Choose subject:", reply_markup=InlineKeyboardMarkup(keyboard))

# --- Callback Handler ---
def button_handler(update, context):
    query = update.callback_query
    query.answer()

    # Primary / Secondary books
    if query.data == "primary_books":
        query.edit_message_text("📕 Primary Books: Coming soon")
    elif query.data == "secondary_books":
        keyboard = [
            [InlineKeyboardButton("Grade 9", url="https://t.me/EthioBookGrade1_12/57?single")],
            [InlineKeyboardButton("Grade 10", url="https://t.me/EthioBookGrade1_12/80?single")],
            [InlineKeyboardButton("Grade 11", url="https://t.me/EthioBookGrade1_12/102?single")],
            [InlineKeyboardButton("Grade 12", callback_data="coming_soon")]
        ]
        query.edit_message_text("📗 Secondary Books:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "primary_guides":
        query.edit_message_text("📘 Primary Guides: Coming soon")
    elif query.data == "secondary_guides":
        keyboard = [
            [InlineKeyboardButton("Grade 9", url="https://t.me/EthioBookGrade1_12/67")],
            [InlineKeyboardButton("Grade 10", url="https://t.me/EthioBookGrade1_12/91?single")],
            [InlineKeyboardButton("Grade 11", url="https://t.me/EthioBookGrade1_12/113?single")],
            [InlineKeyboardButton("Grade 12", url="https://t.me/EthioBookGrade1_12/123?single")]
        ]
        query.edit_message_text("📘 Secondary Teacher Guides:", reply_markup=InlineKeyboardMarkup(keyboard))

    # Entrance Exams
    elif query.data == "entrance_natural":
        keyboard = [
            [InlineKeyboardButton("📐 Maths", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("📖 English", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("🧪 Chemistry", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("⚡ Physics", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("🧬 Biology", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("🧠 Aptitude", url="https://fetena.net/exam/entrance")]
        ]
        query.edit_message_text("🔬 Natural Science Entrance:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "entrance_social":
        keyboard = [
            [InlineKeyboardButton("📐 Maths", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("📖 English", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("⚖ Civics", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("🌍 Geography", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("📜 History", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("💰 Economics", url="https://fetena.net/exam/entrance")],
            [InlineKeyboardButton("🧠 Aptitude", url="https://fetena.net/exam/entrance")]
        ]
        query.edit_message_text("🌍 Social Science Entrance:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "coming_soon":
        query.edit_message_text("⏳ Coming soon...")

# --- Handle Text Inputs ---
def handle_message(update, context):
    text = update.message.text
    if text == "📚 Textbooks":
        handle_textbooks(update, context)
    elif text == "📘 Teacher Guides":
        handle_teacher_guides(update, context)
    elif text == "📝 Entrance Exam":
        handle_entrance(update, context)
    elif text == "🏛 Ministry Exam":
        handle_ministry(update, context)
    else:
        update.message.reply_text("Please use the menu buttons.")

# --- Main ---
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()