from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from attendance import (
    add_record,
    get_start_work_time,
    get_last_open_break_info,
    get_break_totals,
    calculate_late,
    calculate_late_penalty
)

from datetime import datetime
from zoneinfo import ZoneInfo
import os

MENU = [
    ["🟢 Start Work", "🚬 SMK Break"],
    ["🚻 WC Break", "🍽 Lunch Break"],
    ["🍛 Dinner Break", "🔙 Back To Work"],
    ["🔴 Off Work", "📊 My Status"]
]


def now_time():
    return datetime.now(
        ZoneInfo("Asia/Karachi")
    )


async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE):

    keyboard = ReplyKeyboardMarkup(
        MENU,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "Welcome to Panda Attendance System",
        reply_markup=keyboard
    )


async def buttons(update: Update,
                  context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.full_name

    action = update.message.text

    now = now_time()

    time_now = now.strftime("%I:%M %p")
    date_now = now.strftime("%Y-%m-%d")

    # START WORK
    if action == "🟢 Start Work":

        existing = get_start_work_time(
            user,
            date_now
        )

        if existing:
            msg = (
                f"⚠️ {user}\n\n"
                f"You already started work today.\n"
                f"Start Time: {existing}"
            )

        else:

    late_minutes = calculate_late(
        time_now
    )

    penalty = calculate_late_penalty(
        late_minutes
    )

    add_record(
        date_now,
        user,
        "Start Work",
        time_now,
        "",
        "",
        late_minutes,
        penalty
    )

    if late_minutes == 0:

        msg = (
            f"🟢 {user} started work\n\n"
            f"⏰ Start Time: {time_now}\n\n"
            f"✅ On Time"
        )

    else:

        msg = (
            f"🚨 LATE ENTRY\n\n"
            f"👤 {user}\n\n"
            f"⏰ Start Time: {time_now}\n\n"
            f"⌛ Late: {late_minutes} Minutes\n"
            f"💸 Fine: Rs. {penalty}"
        )

    # SMK BREAK
    elif action == "🚬 SMK Break":

        add_record(
            date_now,
            user,
            "Break Start",
            time_now,
            "SMK"
        )

        totals = get_break_totals(
            user,
            date_now
        )

        remaining = max(
            0,
            50 - totals["smk_wc"]
        )

        msg = (
            f"🚬 {user} started SMK Break\n\n"
            f"⏰ Out Time: {time_now}\n\n"
            f"Remaining SMK/WC Time:\n"
            f"{remaining} Minutes"
        )

    # WC BREAK
    elif action == "🚻 WC Break":

        add_record(
            date_now,
            user,
            "Break Start",
            time_now,
            "WC"
        )

        totals = get_break_totals(
            user,
            date_now
        )

        remaining = max(
            0,
            50 - totals["smk_wc"]
        )

        msg = (
            f"🚻 {user} started WC Break\n\n"
            f"⏰ Out Time: {time_now}\n\n"
            f"Remaining SMK/WC Time:\n"
            f"{remaining} Minutes"
        )

    # LUNCH BREAK
    elif action == "🍽 Lunch Break":

        add_record(
            date_now,
            user,
            "Break Start",
            time_now,
            "Lunch"
        )

        totals = get_break_totals(
            user,
            date_now
        )

        remaining = max(
            0,
            90 - totals["lunch"]
        )

        msg = (
            f"🍽 {user} started Lunch Break\n\n"
            f"⏰ Out Time: {time_now}\n\n"
            f"Remaining Lunch Time:\n"
            f"{remaining} Minutes"
        )

    # DINNER BREAK
    elif action == "🍛 Dinner Break":

        add_record(
            date_now,
            user,
            "Break Start",
            time_now,
            "Dinner"
        )

        totals = get_break_totals(
            user,
            date_now
        )

        remaining = max(
            0,
            30 - totals["dinner"]
        )

        msg = (
            f"🍛 {user} started Dinner Break\n\n"
            f"⏰ Out Time: {time_now}\n\n"
            f"Remaining Dinner Time:\n"
            f"{remaining} Minutes"
        )

    # BACK TO WORK
    elif action == "🔙 Back To Work":

        break_type, start_time = get_last_open_break_info(
            user,
            date_now
        )

        if not break_type:

            msg = (
                f"⚠️ {user}\n\n"
                f"No active break found."
            )

        else:

            start_dt = datetime.strptime(
                start_time,
                "%I:%M %p"
            )

            end_dt = datetime.strptime(
                time_now,
                "%I:%M %p"
            )

            minutes_used = int(
                (end_dt - start_dt).total_seconds() / 60
            )

            if minutes_used < 0:
                minutes_used = 0

            add_record(
                date_now,
                user,
                "Break End",
                time_now,
                break_type,
                minutes_used
            )

            totals = get_break_totals(
                user,
                date_now
            )

            if break_type in ["SMK", "WC"]:

                remaining = max(
                    0,
                    50 - totals["smk_wc"]
                )

            elif break_type == "Lunch":

                remaining = max(
                    0,
                    90 - totals["lunch"]
                )

            else:

                remaining = max(
                    0,
                    30 - totals["dinner"]
                )

            msg = (
                f"🔙 {user} returned to work\n\n"
                f"Break Type: {break_type}\n"
                f"Break Used: {minutes_used} Minutes\n\n"
                f"Remaining:\n"
                f"{remaining} Minutes"
            )

    # STATUS
    elif action == "📊 My Status":

        totals = get_break_totals(
            user,
            date_now
        )

        msg = (
            f"📊 Employee Status\n\n"
            f"👤 {user}\n\n"
            f"🚬 + 🚻 Used: {totals['smk_wc']}/50 Minutes\n"
            f"🍽 Lunch Used: {totals['lunch']}/90 Minutes\n"
            f"🍛 Dinner Used: {totals['dinner']}/30 Minutes\n\n"
            f"🚬 + 🚻 Remaining: {max(0, 50 - totals['smk_wc'])} Minutes\n"
            f"🍽 Remaining: {max(0, 90 - totals['lunch'])} Minutes\n"
            f"🍛 Remaining: {max(0, 30 - totals['dinner'])} Minutes"
        )

    # OFF WORK
    elif action == "🔴 Off Work":

        totals = get_break_totals(
            user,
            date_now
        )

        add_record(
            date_now,
            user,
            "Off Work",
            time_now
        )

        msg = (
            f"🔴 {user} finished work\n\n"
            f"⏰ Off Time: {time_now}\n\n"
            f"📋 Daily Report\n\n"
            f"🚬 + 🚻 Used: {totals['smk_wc']}/50 Minutes\n"
            f"🍽 Lunch Used: {totals['lunch']}/90 Minutes\n"
            f"🍛 Dinner Used: {totals['dinner']}/30 Minutes\n\n"
            f"🚬 + 🚻 Remaining: {max(0, 50 - totals['smk_wc'])} Minutes\n"
            f"🍽 Remaining: {max(0, 90 - totals['lunch'])} Minutes\n"
            f"🍛 Remaining: {max(0, 30 - totals['dinner'])} Minutes"
        )

    else:
        msg = f"{user}: {action}"

    await update.message.reply_text(msg)


def main():

    token = os.getenv("BOT_TOKEN")

    app = Application.builder().token(token).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            buttons
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
