from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from attendance import save_attendance

from datetime import datetime
from zoneinfo import ZoneInfo
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

    # Get user's actual Telegram name
    user = update.effective_user.full_name

    action = update.message.text

    # Pakistan Time
    now = datetime.now(ZoneInfo("Asia/Karachi"))

    time_now = now.strftime("%I:%M %p")
    date_now = now.strftime("%Y-%m-%d")

    save_attendance(
        user,
        action,
        time_now,
        date_now
    )

    # START WORK
    if action == "🟢 Start Work":
        msg = (
            f"🟢 {user} started work\n"
            f"⏰ Start Time: {time_now}"
        )

    # SMK BREAK
    elif action == "🚬 SMK Break":
        msg = (
            f"🚬 {user} went for SMK Break\n"
            f"⏰ Out Time: {time_now}"
        )

    # WC BREAK
    elif action == "🚻 WC Break":
        msg = (
            f"🚻 {user} went for WC Break\n"
            f"⏰ Out Time: {time_now}"
        )

    # LUNCH BREAK
    elif action == "🍽 Lunch Break":
        msg = (
            f"🍽 {user} went for Lunch Break\n"
            f"⏰ Out Time: {time_now}"
        )

    # DINNER BREAK
    elif action == "🍛 Dinner Break":
        msg = (
            f"🍛 {user} went for Dinner Break\n"
            f"⏰ Out Time: {time_now}"
        )

    # BACK TO WORK
    elif action == "🔙 Back To Work":
        msg = (
            f"🔙 {user} returned to work\n"
            f"⏰ In Time: {time_now}"
        )

    # OFF WORK
    elif action == "🔴 Off Work":
        msg = (
            f"🔴 {user} finished work\n"
            f"⏰ Off Time: {time_now}"
        )

    # STATUS
    elif action == "📊 My Status":
        msg = (
            f"📊 Employee Status\n"
            f"👤 {user}\n"
            f"⏰ Current Time: {time_now}"
        )

    else:
        msg = f"{user}: {action}"

    await update.message.reply_text(msg)


def main():

    token = os.getenv("BOT_TOKEN")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, buttons)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
