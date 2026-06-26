import json
import os

import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

google_creds = json.loads(
    os.getenv("GOOGLE_CREDENTIALS")
)

CREDS = Credentials.from_service_account_info(
    google_creds,
    scopes=SCOPES
)

client = gspread.authorize(CREDS)

settings_sheet = client.open(
    "Panda Attendence Sheet"
).worksheet("Settings")


def get_settings():
    """
    Returns all settings as a dictionary.
    """

    rows = settings_sheet.get_all_records()

    settings = {}

    for row in rows:
        settings[row["Setting"]] = str(row["Value"])

    return settings


def get_setting(name):
    """
    Returns one setting by name.
    """

    settings = get_settings()

    return settings.get(name)
