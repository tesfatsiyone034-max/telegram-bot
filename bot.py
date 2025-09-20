import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Get bot token from environment variable
TOKEN = os.getenv("BOT_TOKEN")

# --- Links for Textbook and Teacher Guide ---
TEXTBOOK_SECONDARY_LINKS = {
    "Grade9": "https://t.me/EthioBookGrade1_12/57?single",
    "Grade10": "https://t.me/EthioBookGrade1_12/80?single",
    "Grade11": "https://t.me/EthioBookGrade1_12/102?single",
}

TEACHERGUIDE_SECONDARY_LINKS = {
    "Grade9": "https://t.me/EthioBookGrade1_12/67",
    "Grade10": "https://t.me/EthioBookGrade1_12/91?single",
    "Grade11": "https://t.me/EthioBookGrade1_12/113?single",
    "Grade12": "https://t.me/EthioBookGrade1_12/123?single",
}

# --- Entrance Exam ---
ENTRANCE_LINK = "https://fetena.net/exam/entrance"
ENTRANCE_NS_SUBJECTS = ["Maths", "English", "Chemistry", "Physics", "Biology", "Aptitude"]
ENTRANCE_SS_SUBJECTS = ["Maths", "English", "Civics", "Geography", "History", "Economics"]

# --- Ministry Exam ---
MINISTRY_LINK = "https://fetena.net/exam/ministry"
MINISTRY_SUBJECTS = ["Maths", "English", "General Science", "Citizenship", "Social Study"]

# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 Textbook", callback_data="textbook")],
        [InlineKeyboardButton("🧑‍🏫 Teacher Guide", callback_data="teacherguide")],
        [InlineKeyboardButton("📄 Entrance Exam", callback_data="entrance")],
        [InlineKeyboardButton("🏛️ Ministry Exam", callback_data="ministry")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome! Please choose an option:", reply_markup=reply_markup)

# --- Button Handler ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # --- Textbook ---
    if data == "textbook":
        keyboard = [
            [InlineKeyboardButton("📚 Primary Books (Grades 1-8)", callback_data="textbook_primary")],
            [InlineKeyboardButton("🎓 Secondary Books (Grades 9-12)", callback_data="textbook_secondary")]
        ]
        await query.edit_message_text("📘 Choose Primary or Secondary Books:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "textbook_primary":
        await query.edit_message_text("📚 Coming soon")

    elif data == "textbook_secondary":
        keyboard = [
            [InlineKeyboardButton("Grade 9", url=TEXTBOOK_SECONDARY_LINKS["Grade9"])],
            [InlineKeyboardButton("Grade 10", url=TEXTBOOK_SECONDARY_LINKS["Grade10"])],
            [InlineKeyboardButton("Grade 11", url=TEXTBOOK_SECONDARY_LINKS["Grade11"])],
            [InlineKeyboardButton("Grade 12", callback_data="textbook_grade12_coming")]
        ]
        await query.edit_message_text("🎓 Select your grade:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "textbook_grade12_coming":
        await query.edit_message_text("🎓 Coming soon")

    # --- Teacher Guide ---
    elif data == "teacherguide":
        keyboard = [
            [InlineKeyboardButton("📚 Primary Books (Grades 1-8)", callback_data="teacherguide_primary")],
            [InlineKeyboardButton("🎓 Secondary Books (Grades 9-12)", callback_data="teacherguide_secondary")]
        ]
        await query.edit_message_text("🧑‍🏫 Choose Primary or Secondary Books:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "teacherguide_primary":
        await query.edit_message_text("📚 Coming soon")

    elif data == "teacherguide_secondary":
        keyboard = [
            [InlineKeyboardButton("Grade 9", url=TEACHERGUIDE_SECONDARY_LINKS["Grade9"])],
            [InlineKeyboardButton("Grade 10", url=TEACHERGUIDE_SECONDARY_LINKS["Grade10"])],
            [InlineKeyboardButton("Grade 11", url=TEACHERGUIDE_SECONDARY_LINKS["Grade11"])],
            [InlineKeyboardButton("Grade 12", url=TEACHERGUIDE_SECONDARY_LINKS["Grade12"])]
        ]
        await query.edit_message_text("🎓 Select your grade:", reply_markup=InlineKeyboardMarkup(keyboard))

    # --- Entrance Exam ---
    elif data == "entrance":
        keyboard = [
            [InlineKeyboardButton("🧪 Natural Science", callback_data="entrance_ns")],
            [InlineKeyboardButton("🌍 Social Science", callback_data="entrance_ss")]
        ]
        await query.edit_message_text("📄 Choose your exam category:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "entrance_ns":
        keyboard = [[InlineKeyboardButton(subj, url=ENTRANCE_LINK)] for subj in ENTRANCE_NS_SUBJECTS]
        await query.edit_message_text("🧪 Natural Science Subjects:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "entrance_ss":
        keyboard = [[InlineKeyboardButton(subj, url=ENTRANCE_LINK)] for subj in ENTRANCE_SS_SUBJECTS]
        await query.edit_message_text("🌍 Social Science Subjects:", reply_markup=InlineKeyboardMarkup(keyboard))

    # --- Ministry Exam ---
    elif data == "ministry":
        keyboard = [[InlineKeyboardButton(subj, url=MINISTRY_LINK)] for subj in MINISTRY_SUBJECTS]
        await query.edit_message_text("🏛️ Ministry Exam Subjects:", reply_markup=InlineKeyboardMarkup(keyboard))

# --- Build and run bot ---
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()