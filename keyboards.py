from telegram import ReplyKeyboardMarkup

# ==========================
# Employee Menu
# ==========================

EMPLOYEE_MENU = [
    ["🟢 Start Work", "🚬 SMK Break"],
    ["🚻 WC Break", "🍽 Lunch Break"],
    ["🍛 Dinner Break", "🔙 Back To Work"],
    ["🔴 Off Work", "📊 My Status"]
]

# ==========================
# Admin Menu
# ==========================

ADMIN_MENU = [
    ["🟢 Start Work", "🚬 SMK Break"],
    ["🚻 WC Break", "🍽 Lunch Break"],
    ["🍛 Dinner Break", "🔙 Back To Work"],
    ["🔴 Off Work", "📊 My Status"],
    ["🛡 Admin Panel"]
]

# ==========================
# Owner Menu
# ==========================

OWNER_MENU = [
    ["🟢 Start Work", "🚬 SMK Break"],
    ["🚻 WC Break", "🍽 Lunch Break"],
    ["🍛 Dinner Break", "🔙 Back To Work"],
    ["🔴 Off Work", "📊 My Status"],
    ["🛡 Admin Panel", "👑 Owner Panel"]
]


def employee_keyboard():
    return ReplyKeyboardMarkup(
        EMPLOYEE_MENU,
        resize_keyboard=True
    )


def admin_keyboard():
    return ReplyKeyboardMarkup(
        ADMIN_MENU,
        resize_keyboard=True
    )


def owner_keyboard():
    return ReplyKeyboardMarkup(
        OWNER_MENU,
        resize_keyboard=True
    )