import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Read TARGET_TIMEZONE from .env file, default to UTC if not found
    TARGET_TIMEZONE = os.getenv("TARGET_TIMEZONE", "UTC")

    # Read BASE_TIMEZONE from .env file
    BASE_TIMEZONE = os.getenv("BASE_TIMEZONE", "Etc/GMT+5")  # Default to GMT-5

    # Read CRITICAL_TIMES from .env, and split the string into a list of dictionaries
    critical_times_str = os.getenv("CRITICAL_TIMES", "")
    CRITICAL_TIMES = [
        {"day": time.split(",")[0], "time": time.split(",")[1]}
        for time in critical_times_str.split(";") if time
    ]

    # Read BASE_URL from .env file
    BASE_URL = os.getenv("BASE_URL", "https://www.investing.com/economic-calendar/")

    # Parse SCHEDULE_INTERVAL
    raw_interval = os.getenv("SCHEDULE_INTERVAL", "1m").lower()
    INTERVAL_VALUE = None
    INTERVAL_UNIT = None
    if raw_interval.endswith("s"):  # Seconds
        INTERVAL_VALUE = int(raw_interval[:-1])
        INTERVAL_UNIT = "seconds"
    elif raw_interval.endswith("m"):  # Minutes
        INTERVAL_VALUE = int(raw_interval[:-1])
        INTERVAL_UNIT = "minutes"
    elif raw_interval.endswith("h"):  # Hours
        INTERVAL_VALUE = int(raw_interval[:-1])
        INTERVAL_UNIT = "hours"
    elif raw_interval.endswith("d"):  # Days
        INTERVAL_VALUE = int(raw_interval[:-1])
        INTERVAL_UNIT = "days"
    else:
        INTERVAL_VALUE = 1
        INTERVAL_UNIT = "minutes"  # Default to 1 minute

    # Read PRINT_TABLE and convert to boolean
    PRINT_TABLE = os.getenv("PRINT_TABLE", "False").lower() == "true"

    # Read PRINT_CURRENCIES and parse into a list
    raw_currencies = os.getenv("PRINT_CURRENCIES", "ALL")
    PRINT_CURRENCIES = (
        None if raw_currencies.upper() == "ALL" else raw_currencies.split(",")
    )

    # Use colors in the output table
    USE_COLORS = os.getenv("USE_COLORS", "True").lower() == "true"
