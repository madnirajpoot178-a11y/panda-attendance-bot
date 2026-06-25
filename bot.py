from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os

MENU = [
    ["🟢 Start Work", "🚬 SMK Break"],
    ["🚻 WC Break", "🍽 Lunch Break"],
    ["🍛 Dinner Break", "🔙 Back To Work"],
    ["🔴 Off Work", "📊 My Status"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text(
        "Welcome to Panda Attendance System",
        reply_markup=keyboard
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username or update.effective_user.first_name
    text = update.message.text

    await update.message.reply_text(
        f"✅ @{user} clicked: {text}"
    )

def main():
    token = os.getenv("BOT_TOKEN")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buttons))

    app.run_polling()

if __name__ == "__main__":
    main()
