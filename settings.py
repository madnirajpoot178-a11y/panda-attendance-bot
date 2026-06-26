import os
import json
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

    rows = settings_sheet.get_all_records()

    data = {}

    for row in rows:

        key = str(row["Setting"]).strip()

        value = str(row["Value"]).strip()

        data[key] = value

    return data


def office_start():

    return get_settings()["Office Start"]


def office_end():

    return get_settings()["Office End"]


def late_fine_per_minute():

    return int(
        get_settings()["Late Fine Per Minute"]
    )


def break_fine():

    return int(
        get_settings()["Break Fine"]
    )


def smk_wc_limit():

    return int(
        get_settings()["SMK WC Limit"]
    )


def lunch_limit():

    return int(
        get_settings()["Lunch Limit"]
    )


def dinner_limit():

    return int(
        get_settings()["Dinner Limit"]
    )


def friday_lunch_start():

    return get_settings()["Friday Lunch Start"]


def friday_lunch_end():

    return get_settings()["Friday Lunch End"]


def half_day_start():

    return get_settings()["Half Day Start"]


def half_day_end():

    return get_settings()["Half Day End"]
