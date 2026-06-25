import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file(
    "vocal-affinity-500511-m8-a1b6e071f727.json",
    scopes=SCOPES
)

client = gspread.authorize(CREDS)
sheet = client.open("Panda Attendance").sheet1

def save_attendance(username, action):
    now = datetime.now()

    sheet.append_row([
        now.strftime("%Y-%m-%d"),
        username,
        action,
        now.strftime("%H:%M:%S")
    ])

def get_today_start(username):
    records = sheet.get_all_values()

    today = datetime.now().strftime("%Y-%m-%d")

    for row in records:
        if len(row) >= 4:
            if row[0] == today and row[1] == username and row[2] == "🟢 Start Work":
                return row[3]

    return None
