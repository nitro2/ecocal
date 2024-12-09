import os
import argparse
from utils import prettify_dataset
from fetcher import Fetcher
from config import Config

def test_sample_html_parsing(input_file):
    """
    Test parsing of the sample HTML file provided as input.
    """
    # Check if the sample file exists
    if not os.path.exists(input_file):
        print(f"Sample file not found: {input_file}")
        return

    fetcher = Fetcher(Config.BASE_URL, target_timezone=Config.TARGET_TIMEZONE)
    data = fetcher.read_data(input_file)

    # Print the parsed data for verification
    # print("Parsed data from sample HTML:")
    # for entry in parsed_data:
    #     print(entry)
    prettify_dataset(data)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Parse a sample economic calendar HTML file.")
    parser.add_argument("input_file", help="Path to the sample HTML file")
    args = parser.parse_args()

    # Run the parsing function with the provided file
    test_sample_html_parsing(args.input_file)

if __name__ == "__main__":
    main()
