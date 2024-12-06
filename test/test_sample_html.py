import os
import argparse
from utils import load_html_from_file, prettify_rows
from fetcher import Fetcher

def test_sample_html_parsing(input_file):
    """
    Test parsing of the sample HTML file provided as input.
    """
    # Check if the sample file exists
    if not os.path.exists(input_file):
        print(f"Sample file not found: {input_file}")
        return

    # Load the sample HTML
    soup = load_html_from_file(input_file)
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
    fetcher = Fetcher("https://www.investing.com/economic-calendar/", target_timezone="Asia/Ho_Chi_Minh")  # URL is not used here
    parsed_data = fetcher._extract_data(rows)

    # Print the parsed data for verification
    # print("Parsed data from sample HTML:")
    # for entry in parsed_data:
    #     print(entry)
    prettify_rows(parsed_data)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Parse a sample economic calendar HTML file.")
    parser.add_argument("input_file", help="Path to the sample HTML file")
    args = parser.parse_args()

    # Run the parsing function with the provided file
    test_sample_html_parsing(args.input_file)

if __name__ == "__main__":
    main()
