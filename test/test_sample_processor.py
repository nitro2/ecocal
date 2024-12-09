import sys
import os
from fetcher import Fetcher
from processor import SignalProcessor
from utils import prettify_dataset
from config import Config

import os
import argparse
from utils import prettify_dataset
from fetcher import Fetcher

def test_sample_processor(input_file):
    """
    Test parsing of the sample HTML file provided as input.
    """
    # Check if the sample file exists
    if not os.path.exists(input_file):
        print(f"Sample file not found: {input_file}")
        return


    fetcher = Fetcher(Config.BASE_URL, target_timezone=Config.TARGET_TIMEZONE)
    dataset = fetcher.read_data(input_file)
    processor = SignalProcessor()

    # Aggregate signals and prettify rows
    aggregated_signal = processor.aggregate_signals(dataset)
    print(f"Overall Signal: {aggregated_signal}")



def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Parse a sample economic calendar HTML file.")
    parser.add_argument("input_file", help="Path to the sample HTML file")
    args = parser.parse_args()

    # Run the parsing function with the provided file
    test_sample_processor(args.input_file)

if __name__ == "__main__":
    main()
