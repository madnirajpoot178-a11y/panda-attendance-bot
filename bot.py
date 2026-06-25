from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from attendance import save_attendance, get_user_session

from datetime import datetime
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
    action = update.message.text

    now = datetime.now()
    session = get_user_session(user)

    save_attendance(
        user,
        action,
        now.strftime("%H:%M:%S"),
        now.strftime("%Y-%m-%d")
    )

    # START WORK
    if action == "🟢 Start Work":

        if session["start_work"] is not None:
            await update.message.reply_text(
                f"⚠️ Work already started at {session['start_work'].strftime('%I:%M %p')}"
            )
            return

        session["start_work"] = now

        await update.message.reply_text(
            f"🟢 Work Started\n\nStart Time: {now.strftime('%I:%M %p')}"
        )

    # BREAK START
    elif action in ["🚬 SMK Break", "🚻 WC Break", "🍽 Lunch Break", "🍛 Dinner Break"]:

        session["break_start"] = now

        await update.message.reply_text(
            f"{action}\n\nStarted: {now.strftime('%I:%M %p')}"
        )

    # BACK TO WORK
    elif action == "🔙 Back To Work":

        if session["break_start"] is None:
            await update.message.reply_text(
                "⚠️ No active break found."
            )
            return

        minutes = int(
            (now - session["break_start"]).total_seconds() / 60
        )

        session["total_break_minutes"] += minutes
        session["break_start"] = None

        await update.message.reply_text(
            f"🔙 Back To Work\n\nBreak Duration: {minutes} min\n\nTotal Break Time Today: {session['total_break_minutes']} min"
        )

    # MY STATUS
    elif action == "📊 My Status":

        if session["start_work"] is None:
            await update.message.reply_text(
                "⚠️ Work not started yet."
            )
            return

        work_minutes = int(
            (now - session["start_work"]).total_seconds() / 60
        )

        await update.message.reply_text(
            f"📊 Today's Status\n\n"
            f"Start Work: {session['start_work'].strftime('%I:%M %p')}\n"
            f"Total Work Time: {work_minutes} min\n"
            f"Total Break Time: {session['total_break_minutes']} min"
        )

    # OFF WORK
    elif action == "🔴 Off Work":

        if session["start_work"] is None:
            await update.message.reply_text(
                "⚠️ Work not started today."
            )
            return

        total_minutes = int(
            (now - session["start_work"]).total_seconds() / 60
        )

        working_minutes = total_minutes - session["total_break_minutes"]

        await update.message.reply_text(
            f"📋 Daily Report\n\n"
            f"Start Work: {session['start_work'].strftime('%I:%M %p')}\n"
            f"Off Work: {now.strftime('%I:%M %p')}\n\n"
            f"Total Shift: {total_minutes} min\n"
            f"Total Break: {session['total_break_minutes']} min\n"
            f"Actual Working Time: {working_minutes} min"
        )

        session["start_work"] = None
        session["break_start"] = None
        session["total_break_minutes"] = 0

    else:

        await update.message.reply_text(
            f"✅ @{user} clicked: {action}"
        )


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
