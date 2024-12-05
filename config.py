import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Read TARGET_TIMEZONE from .env file, default to UTC if not found
    TARGET_TIMEZONE = os.getenv("TARGET_TIMEZONE", "UTC")

    # Read CRITICAL_TIMES from .env, and split the string into a list of dictionaries
    critical_times_str = os.getenv("CRITICAL_TIMES", "")
    CRITICAL_TIMES = [
        {"day": time.split(",")[0], "time": time.split(",")[1]}
        for time in critical_times_str.split(";") if time
    ]

    # Read BASE_URL from .env file
    BASE_URL = os.getenv("BASE_URL", "https://www.investing.com/economic-calendar/")