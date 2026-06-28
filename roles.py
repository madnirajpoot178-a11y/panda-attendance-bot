# ==========================
# Panda Attendance Roles
# ==========================

# Replace with your Telegram ID
OWNER_ID = 8835391677

# Admin IDs
ADMIN_IDS = [
    6632024382,
]

# --------------------------

def is_owner(user_id):
    return user_id == OWNER_ID


def is_admin(user_id):
    return user_id == OWNER_ID or user_id in ADMIN_IDS


def is_employee(user_id):
    return not is_admin(user_id)