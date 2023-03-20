from os import getenv
from dotenv import load_dotenv
from pandas import DataFrame, concat
from gspread import Worksheet, authorize
from gspread.exceptions import WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials as sac

load_dotenv()
AUTH_PROVIDER = "https://www.googleapis.com/oauth2/v1/certs"
GOOGLE_SHEETS_CREDENTIALS = {
    "type": "service_account",
    "project_id": "gymworkout",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": AUTH_PROVIDER,
    "private_key_id": getenv("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": getenv("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": getenv("GOOGLE_CLIENT_EMAIL"),
    "client_id": getenv("GOOGLE_CLIENT_ID"),
    "client_x509_cert_url": getenv("GOOGLE_CLIENT_X509_CERT_URL"),
}


def connect_gsheets(gsheets_url: str, credentials: dict) -> Worksheet:
    FEEDS = "https://spreadsheets.google.com/feeds"
    client = sac.from_json_keyfile_dict(credentials, FEEDS)
    session = authorize(client)
    book = session.open_by_url(gsheets_url)
    return book


def read_gsheets(gsheets_url: str, sheets_to_read: list) -> DataFrame:
    """
    Fetch data from Google Sheets

    Args:
        gsheets_url: string, full link of GSheets file
        sheets_to_read: list-like object of string sheet names

    Returns:
        DataFrame, append of all sheets specified from Google Sheets
    """

    book = connect_gsheets(gsheets_url, GOOGLE_SHEETS_CREDENTIALS)

    df = DataFrame()
    for sheet in sheets_to_read:
        try:
            data = book.worksheet(sheet)
            sheets_data = DataFrame(data.get_values())

            sheets_data.rename(columns=sheets_data.iloc[0], inplace=True)
            sheets_data.drop(sheets_data.index[0], inplace=True)

            df = concat([df, sheets_data], axis=0)

        except WorksheetNotFound:
            print(f'Sheetname: "{sheet}" was not found at\n{gsheets_url}')
    return df


def update_sheet(gsheets_url: str, sheet_name: str, data: DataFrame) -> None:
    book = connect_gsheets(gsheets_url, GOOGLE_SHEETS_CREDENTIALS)

    try:
        sheet = book.worksheet(sheet_name)
    except WorksheetNotFound:
        print(f'Sheetname: "{sheet}" was not found at\n{gsheets_url}')

    sheet.update([data.columns.values.tolist()] + data.values.tolist())
