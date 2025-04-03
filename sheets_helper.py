import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet_data():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    creds_json = json.loads(os.environ.get("GOOGLE_CREDS"))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Patients").sheet1
    return sheet.get_all_records()

def find_patient(input_text):
    data = get_sheet_data()
    for row in data:
        if (
            input_text.lower() == str(row.get("prenom", "")).lower()
            or input_text.lower() == str(row.get("email", "")).lower()
        ):
            return row
    return None