import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

class Config:
    # Read TARGET_TIMEZONE from .env file, default to UTC if not found
    TARGET_TIMEZONE = os.getenv("TARGET_TIMEZONE", "UTC")

    # Read BASE_TIMEZONE from .env file
    BASE_TIMEZONE = os.getenv("BASE_TIMEZONE", "Etc/GMT+5")  # Default to GMT-5

    # Read CRITICAL_TIMES from .env, and split the string into a list of dictionaries
    critical_times_str = os.getenv("CRITICAL_TIMES", "")
    CRITICAL_TIMES = [
        {
            "day": time.split(",")[0].lower(),
            "time": time.split(",")[1]  # Expecting H:M:S format
        }
        for time in critical_times_str.split(";") if time
    ]

    # Read BASE_URL from .env file
    BASE_URL = os.getenv("BASE_URL", "https://www.investing.com/economic-calendar/")

    # Parse default interval
    default_interval_raw = os.getenv("SCHEDULE_INTERVAL_DEFAULT", "10s").lower()
    DEFAULT_INTERVAL_VALUE, DEFAULT_INTERVAL_UNIT = None, None
    if default_interval_raw.endswith("s"):  # Seconds
        DEFAULT_INTERVAL_VALUE = int(default_interval_raw[:-1])
        DEFAULT_INTERVAL_UNIT = "seconds"
    elif default_interval_raw.endswith("m"):  # Minutes
        DEFAULT_INTERVAL_VALUE = int(default_interval_raw[:-1])
        DEFAULT_INTERVAL_UNIT = "minutes"

    # Parse critical interval
    critical_interval_raw = os.getenv("SCHEDULE_INTERVAL_CRITICAL", "3s").lower()
    CRITICAL_INTERVAL_VALUE, CRITICAL_INTERVAL_UNIT = None, None
    if critical_interval_raw.endswith("s"):  # Seconds
        CRITICAL_INTERVAL_VALUE = int(critical_interval_raw[:-1])
        CRITICAL_INTERVAL_UNIT = "seconds"
    elif critical_interval_raw.endswith("m"):  # Minutes
        CRITICAL_INTERVAL_VALUE = int(critical_interval_raw[:-1])
        CRITICAL_INTERVAL_UNIT = "minutes"

    # Read PRINT_TABLE and convert to boolean
    PRINT_TABLE = os.getenv("PRINT_TABLE", "False").lower() == "true"

    # Read PRINT_CURRENCIES and parse into a list
    raw_currencies = os.getenv("PRINT_CURRENCIES", "ALL")
    PRINT_CURRENCIES = (
        None if raw_currencies.upper() == "ALL" else raw_currencies.split(",")
    )

    # Use colors in the output table
    USE_COLORS = os.getenv("USE_COLORS", "True").lower() == "true"

    IMPORTANCE_FILTER = int(os.getenv('IMPORTANCE_FILTER', 1))