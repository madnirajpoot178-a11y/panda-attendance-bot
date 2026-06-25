import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file(
    "vocal-affinity-500511-m8-a1b6e071f727.json",
    scopes=SCOPES
)

client = gspread.authorize(CREDS)

# IMPORTANT: This must match your Google Sheet name exactly
sheet = client.open("Panda Attendance Sheet").sheet1


def save_attendance(username, action, time_now, date_now):
    sheet.append_row([
        date_now,
        username,
        action,
        time_now
    ])
