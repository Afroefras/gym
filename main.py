from utils.import_data import read_gsheets, update_sheet

BASE_URL = "https://docs.google.com/spreadsheets/d/"
FILE_ID = "1JzO3I-fjgqreIvRjZTEY1XhpXRqa7abAPWQovw2U9v4"
URL = BASE_URL + FILE_ID


def clean_workout() -> None:
    df = read_gsheets(URL, ["Workout"])
    df.replace({"": None}, inplace=True)
    df.fillna(method="ffill", inplace=True)
    update_sheet(URL, "Workout", df)


if __name__ == "__main__":
    clean_workout()
