import logging
from datetime import datetime
from bs4 import BeautifulSoup
from tabulate import tabulate

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_error(message):
    """
    Logs an error message to the console with a timestamp.
    :param message: The error message to log.
    """
    logging.error(message)

def log_info(message):
    """
    Logs an informational message to the console with a timestamp.
    :param message: The informational message to log.
    """
    logging.info(message)

def parse_time(time_str, format="%H:%M"):
    """
    Parses a time string into a datetime object.
    :param time_str: The time string to parse (e.g., "22:00").
    :param format: The expected format of the time string.
    :return: A datetime object representing the parsed time.
    """
    try:
        return datetime.strptime(time_str, format).time()
    except ValueError as e:
        log_error(f"Time parsing error: {e}")
        return None

def load_html_from_file(file_path):
    """
    Load and parse HTML content from a file.
    :param file_path: Path to the HTML file.
    :return: BeautifulSoup object or None if loading fails.
    """
    try:
        with open(file_path, "rb") as file:
            html = file.read()
        return BeautifulSoup(html, "html.parser")
    except Exception as e:
        log_error(f"Failed to load HTML from {file_path}: {e}")
        return None

def prettify_rows(rows, signals=None):
    """
    Prettify and print rows with alignment for console output.
    :param rows: List of dictionaries containing row data.
    :param signals: Optional list of signals corresponding to each row.
    """
    headers = ["time", "currency", "event", "actual", "forecast", "previous", "signal"]

    # Prepare rows for tabulation
    table_data = []
    for idx, row in enumerate(rows):
        signal = signals[idx] if signals else "_"
        table_data.append([
            row.get("time", "_"),
            row.get("currency", "_"),
            row.get("event", "_"),
            row.get("actual", "_") if row.get("actual") is not None else "_",
            row.get("forecast", "_") if row.get("forecast") is not None else "_",
            row.get("previous", "_") if row.get("previous") is not None else "_",
            signal.value,
        ])

    # Print the formatted table
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
