import json
import sys
from config import Config
from fetcher import Fetcher

def export_event_ids(input_html, output_json):
    """
    Export event IDs, names, and currency from the parsed data using Fetcher's read_data method to a JSON template.
    :param input_html: Path to the input HTML file.
    :param output_json: Path to save the JSON template.
    """
    # Initialize Fetcher
    fetcher = Fetcher(Config.BASE_URL, target_timezone=Config.TARGET_TIMEZONE)

    # Get data from the sample HTML using Fetcher's read_data method
    rows = fetcher.read_data(input_html)  # Pass the input file as an argument

    # Create a dictionary for event data
    events = {}
    for row in rows:
        try:
            # Extract event_id, event_name, and currency
            event_id = row.get('id', None)
            event_name = row.get('event', 'Unknown Event')
            currency = row.get('currency', 'USD')  # Default to 'USD' if not found

            # Remove the specific month and year from the event name
            event_name = event_name.split("(")[0].strip()

            if event_id:
                # Add to the dictionary with the desired structure, including currency
                events[event_id] = {
                    "event": event_name,
                    "currency": currency,  # Extracted from the fetcher
                    "pn_indicator": ""  # Placeholder for manual editing
                }
        except Exception as e:
            print(f"Error extracting event data: {e}")

    # Save the event data to a JSON file
    with open(output_json, "w") as json_file:
        json.dump(events, json_file, indent=4)
    print(f"Event data exported to {output_json}")

if __name__ == "__main__":
    # python3 export_event_ids.py sample/economic_calendar.html event_data_template.json

    # Ensure that the input HTML file and output JSON file are provided
    if len(sys.argv) != 3:
        print("Usage: python3 export_event_ids.py <input_html_file> <output_json_file>")
        sys.exit(1)

    # Get input HTML file and output JSON file from command line arguments
    input_html = sys.argv[1]
    output_json = sys.argv[2]

    # Export event IDs
    export_event_ids(input_html, output_json)
