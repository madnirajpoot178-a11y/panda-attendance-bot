import os
import json
import gspread

from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Read credentials from Railway Variable
google_creds = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

CREDS = Credentials.from_service_account_info(
    google_creds,
    scopes=SCOPES
)

client = gspread.authorize(CREDS)

# Your Google Sheet Name
sheet = client.open("Panda Attendence Sheet").sheet1


def save_attendance(username, action, time_now, date_now):
    sheet.append_row([
        date_now,
        username,
        action,
        time_now
    ])
