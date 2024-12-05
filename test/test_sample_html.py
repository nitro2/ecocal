import os
from utils import load_html_from_file
from fetcher import Fetcher

def test_sample_html_parsing():
    """
    Test parsing of the sample HTML file saved locally.
    """
    # Path to the sample HTML file
    sample_file_path = "sample/economic_calendar.html"

    # Check if the sample file exists
    if not os.path.exists(sample_file_path):
        print(f"Sample file not found: {sample_file_path}")
        return

    # Load the sample HTML
    soup = load_html_from_file(sample_file_path)
    if not soup:
        print("Failed to load or parse the sample HTML file.")
        return

    # Simulate the Fetcher processing the loaded HTML
    table = soup.find('table', {"id": "economicCalendarData"})
    if not table:
        print("Economic calendar table not found in the sample file.")
        return

    # Extract rows from the table
    rows = table.find_all('tr', {"class": "js-event-item"})
    fetcher = Fetcher("https://www.investing.com/economic-calendar/")  # URL is not used here
    parsed_data = fetcher._filter_us_data(rows)

    # Print the parsed data for verification
    print("Parsed data from sample HTML:")
    for entry in parsed_data:
        print(entry)

if __name__ == "__main__":
    test_sample_html_parsing()
