import os
from utils import load_html_from_file
from fetcher import Fetcher

def test_html_parsing():
    sample_path = "sample/economic_calendar.html"

    # Test loading and parsing saved HTML
    if os.path.exists(sample_path):
        soup = load_html_from_file(sample_path)
        if soup:
            table = soup.find('table', {"id": "economicCalendarData"})
            if table:
                print("Table found in saved HTML!")
            else:
                print("Table not found in saved HTML.")
        else:
            print("Failed to parse saved HTML.")
    else:
        print(f"Sample file {sample_path} not found. Run Fetcher with save_sample=True.")

if __name__ == "__main__":
    # Uncomment the following to fetch and save a sample file
    # fetcher = Fetcher("https://www.investing.com/economic-calendar/")
    # fetcher.fetch_data(save_sample=True)

    test_html_parsing()
