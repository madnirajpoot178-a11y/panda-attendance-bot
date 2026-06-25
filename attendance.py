import os
import json
import gspread

from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

google_creds = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

CREDS = Credentials.from_service_account_info(
    google_creds,
    scopes=SCOPES
)

client = gspread.authorize(CREDS)

sheet = client.open("Panda Attendence Sheet").sheet1


def add_record(date_now, username, action, time_now,
               break_type="", minutes=""):

    sheet.append_row([
        date_now,
        username,
        action,
        time_now,
        break_type,
        minutes
    ])


def get_all_records():
    return sheet.get_all_records()


def get_user_today_records(username, date_now):

    rows = get_all_records()

    result = []

    for row in rows:

        if (
            str(row["Date"]) == str(date_now)
            and str(row["Username"]) == str(username)
        ):
            result.append(row)

    return result


def get_last_open_break(username, date_now):

    records = get_user_today_records(
        username,
        date_now
    )

    break_type = None

    for row in records:

        if row["Action"] == "Break Start":
            break_type = row["Break Type"]

        elif row["Action"] == "Break End":
            break_type = None

    return break_type


def get_start_work_time(username, date_now):

    records = get_user_today_records(
        username,
        date_now
    )

    for row in records:

        if row["Action"] == "Start Work":
            return row["Time"]

    return None


def get_break_totals(username, date_now):

    records = get_user_today_records(
        username,
        date_now
    )

    smk_wc = 0
    lunch = 0
    dinner = 0

    for row in records:

        if row["Action"] != "Break End":
            continue

        try:
            minutes = int(row["Minutes"])
        except:
            minutes = 0

        break_type = row["Break Type"]

        if break_type in ["SMK", "WC"]:
            smk_wc += minutes

        elif break_type == "Lunch":
            lunch += minutes

        elif break_type == "Dinner":
            dinner += minutes

    return {
        "smk_wc": smk_wc,
        "lunch": lunch,
        "dinner": dinner
    }
