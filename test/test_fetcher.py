import sys
import os

# Add the parent directory (project folder) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fetcher import Fetcher
from config import Config

def test_fetcher():
    base_url = Config.BASE_URL 
    fetcher = Fetcher(base_url, target_timezone="Asia/Ho_Chi_Minh")

    print("Fetching data...")
    data = fetcher.fetch_data()

    if data:
        print("Data fetched successfully:")
        for entry in data:
            print(entry)
    else:
        print("No data fetched or an error occurred.")

if __name__ == "__main__":
    test_fetcher()
