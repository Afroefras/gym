from numpy import nan
from unicodedata import normalize
from re import UNICODE, sub, search as re_search
from difflib import SequenceMatcher, get_close_matches


def clean_number(clean, to_int: bool = False) -> None:
    """
    Returns None if the input is null-like, else
    cleans everything that is not a number or "."

    Args:
        clean: object to clean, it should represent a number
        to_int: boolean arg to convert it to int or keep float

    Returns: clean number
    """

    clean = sub(r"[^0-9\.]", "", str(clean))
    if clean in {None, nan, "", "nan", "None", "null"}:
        return None

    clean = float(clean)
    if to_int:
        clean = int(clean)
    return clean


def clean_text(text: str, patt: str = r"[^a-zA-Z0-9\s]", lower=True) -> str:
    """
    It replaces accents with their unaccented versions,
    removes special characters, keeps just one space max and
    optionally makes the text lowercase.
    It also checks if the resulting text is empty and returns nan if it is.

    Args:
        text: string to clean
        pattern: regex string pattern to keep, default means it will
            remove every character not present inside [^...]
        lower: boolean to transform the cleaned text into lowercase or not

    Returns: string cleaned text
    """

    clean = normalize("NFD", str(text).replace("\n", " \n "))
    clean = clean.encode("ascii", "ignore")
    clean = sub(patt, " ", clean.decode("utf-8"), flags=UNICODE)
    clean = sub(r"\s{2,}", " ", clean.strip())
    if lower:
        clean = clean.lower()
    if clean in ("", "nan"):
        clean = nan
    return clean


def give_options(
    text: str,
    valid_options: list,
    max_options: int,
    similarity: float = 0.6,
    return_first: float = 0.95,
) -> list:
    """
    Gets the N most similar options from a text provided

    Args:
        text: string to search similarity with
        valid_options: list of correct options to search into
        max_options: int number to fetch the N options
        similarity: float number score, options that don't get at least
            that score, are ignored
        return_first: float number score to return just the first option
            if the score is at least that number

    Returns: list with the N most similar options
    """

    if text in {None, nan, "", "nan", "None", "null"}:
        return [None]

    clean = clean_text(text, lower=True)
    clean_options = map(clean_text, valid_options)
    options_dict = dict(zip(clean_options, valid_options))

    closest_clean_options = get_close_matches(
        clean, clean_options, n=max_options, cutoff=similarity
    )

    closest_clean_options.extend(
        [x for x in clean_options if re_search(f".*{clean}.*", x)]
    )

    closest_options = []
    for x in closest_clean_options:
        if x not in map(lambda x: clean_text(x, lower=True), closest_options):
            closest_options.append(options_dict[x])

    if len(closest_options) == 0:
        return [text]

    if SequenceMatcher(None, text, closest_options[0]).ratio() > return_first:
        return [closest_options[0]]
    else:
        return closest_options[:max_options]
