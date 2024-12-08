import logging
from datetime import datetime
from bs4 import BeautifulSoup
from tabulate import tabulate
from colorama import Fore, Style
from pytz import timezone
from config import Config

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

def convert_time_to_timezone(time_str):
    """
    Convert a time string from the base timezone to the target timezone specified in Config.
    :param time_str: Time string (e.g., "15:30").
    :return: Converted time string in the target timezone.
    """
    try:
        base_tz = timezone(Config.BASE_TIMEZONE)  # Use BASE_TIMEZONE from .env
        target_tz = timezone(Config.TARGET_TIMEZONE) # Use TARGET_TIMEZONE from .env

        # Add today's date to the time string to avoid year 1900 issues
        today = datetime.now().date()
        datetime_with_date = datetime.strptime(f"{today} {time_str}", "%Y-%m-%d %H:%M")

        # Localize the datetime object to the base timezone
        localized_time = base_tz.localize(datetime_with_date, is_dst=None)

        # Convert to the target timezone
        target_time = localized_time.astimezone(target_tz)

        # Return formatted time string
        return target_time.strftime("%H:%M")
    except Exception as e:
        print(f"Error in time conversion: {e}")
        return time_str  # Return original time if conversion fails

def prettify_rows(rows):
    """
    Prettify and print rows with alignment for console output, including color handling for Value objects.
    :param rows: List of dictionaries containing row data.
    """
    # Apply currency filter
    rows = [
        row
        for row in rows
        if (Config.PRINT_CURRENCIES and row.get("currency") in Config.PRINT_CURRENCIES)
            and (Config.IMPORTANCE_FILTER and row.get("importance") >= Config.IMPORTANCE_FILTER)
    ]

    # If no rows match the filter, exit early
    if not rows:
        print("No rows to display after applying currency filter.")
        return

    # Define headers
    headers = ["Time", "Curr", "Imp.", "Event", "Actual", "Forecast", "Previous", "Signal", "P/N"]

    # Prepare table data
    table_data = []
    for idx, row in enumerate(rows):
        # Style importance
        importance = "*" * row.get("importance", 0)
        if Config.USE_COLORS:
            if row.get("importance", 0) == 3:
                importance = Fore.RED + importance + Style.RESET_ALL
            elif row.get("importance", 0) == 2:
                importance = Fore.YELLOW + importance + Style.RESET_ALL
            elif row.get("importance", 0) == 1:
                importance = Fore.GREEN + importance + Style.RESET_ALL

        # Style signal
        signal = row.get("signal", "")
        if Config.USE_COLORS:
            if signal == "Strong Buy":
                signal = Fore.GREEN + signal + Style.RESET_ALL
            elif signal == "Strong Sell":
                signal = Fore.RED + signal + Style.RESET_ALL

        # Style event
        event = row.get("event", "_")
        if Config.USE_COLORS:
            event = Fore.CYAN + event + Style.RESET_ALL

        # Extract and style Actual, Forecast, and Previous values
        def format_value(value_obj):
            if not value_obj:
                return "_"
            value = str(value_obj.value) + value_obj.unit if value_obj.value is not None else ""
            if Config.USE_COLORS:
                if value_obj.color == "positive":
                    value = Fore.GREEN + value + Style.RESET_ALL
                elif value_obj.color == "negative":
                    value = Fore.RED + value + Style.RESET_ALL
                elif value_obj.color == "equal":
                    value = Fore.YELLOW + value + Style.RESET_ALL
            return value

        actual = format_value(row.get("actual"))
        forecast = format_value(row.get("forecast"))
        previous = format_value(row.get("previous"))

        pn_indicator = row.get("pn_indicator", "")
        if Config.USE_COLORS:
            # if pn_indicator == "Positive":
                # pn_indicator = Fore.GREEN + pn_indicator + Style.RESET_ALL
            if pn_indicator == "Negative":
                pn_indicator = Fore.RED + pn_indicator + Style.RESET_ALL

        # Add row to table
        table_data.append([
            row.get("time", "_"),
            row.get("currency", "_"),
            importance,
            event,
            actual,
            forecast,
            previous,
            signal,
            pn_indicator

        ])

    # Print the formatted table if PRINT_TABLE is True
    if Config.PRINT_TABLE:
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

