import os
import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from utils import log_error
from datetime import datetime
from pytz import timezone

class Fetcher:
    def __init__(self, base_url, target_timezone="UTC"):
        """
        Initialize Fetcher with the base URL and target timezone.
        :param base_url: The URL of the economic calendar on Investing.com.
        :param target_timezone: The target timezone for output times (e.g., "UTC").
        """
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.target_timezone = target_timezone

    def extract_data(self, rows):
        """
        Extract relevant information from the rows, including importance level.
        :param rows: List of HTML rows from the economic calendar table.
        :return: List of dictionaries containing extracted data.
        """
        extracted_data = []
        for row in rows:
            try:
                # Extract currency
                currency_cell = row.find('td', {"class": "flagCur"})
                currency = currency_cell.text.strip() if currency_cell else None

                # Extract time
                time_cell = row.find('td', {"class": "first left time"}) or row.find('td', {"class": "time"})
                time = time_cell.text.strip() if time_cell else None

                # Extract event
                event_cell = row.find('td', {"class": "event"})
                event = event_cell.text.strip() if event_cell else "Unknown Event"

                # Extract importance level
                importance_cell = row.find('td', {"class": "sentiment"})
                if importance_cell:
                    importance = len(importance_cell.find_all("i", {"class": "grayFullBullishIcon"}))
                else:
                    importance = 0  # Default to 0 if importance level is missing

                # Extract actual, forecast, and previous values
                actual_cell = row.find('td', {"class": "bold"})
                forecast_cell = row.find('td', {"class": "fore"})
                previous_cell = row.find('td', {"class": "prev"})

                actual = self._parse_value(actual_cell.text.strip()) if actual_cell else None
                forecast = self._parse_value(forecast_cell.text.strip()) if forecast_cell else None
                previous = self._parse_value(previous_cell.text.strip()) if previous_cell else None

                # Append parsed data
                extracted_data.append({
                    "time": time,
                    "currency": currency,
                    "event": event,
                    "importance": importance,
                    "actual": actual,
                    "forecast": forecast,
                    "previous": previous,
                })
            except Exception as e:
                log_error(f"Error parsing row: {e}")

        return extracted_data

    def _parse_value(self, value):
        """
        Convert string values to appropriate numerical format.
        :param value: Raw value string from the table (e.g., "6.3%", "1,000").
        :return: Parsed float or None if parsing fails.
        """
        try:
            # Remove common formatting characters like commas and percentages
            return float(value.replace(',', '').replace('%', ''))
        except ValueError:
            return None

    def fetch_html(self, save_sample=False):
        """
        Fetch HTML content from the base URL.
        :param save_sample: If True, save fetched HTML content to a file.
        :return: BeautifulSoup object containing the parsed HTML.
        """
        try:
            req = urllib.request.Request(self.base_url, headers=self.headers)
            response = urllib.request.urlopen(req)
            html = response.read()

            # Optionally save fetched HTML to a file
            if save_sample:
                file_path = f"sample/economic_calendar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                self.save_html_to_file(html, file_path)

            soup = BeautifulSoup(html, "html.parser")

            return soup
        except HTTPError as e:
            log_error(f"HTTP Error: {e.code}")
        except Exception as e:
            log_error(f"Error fetching data: {e}")
        return []
    
    def fetch_data(self, save_sample=False):
        """
        Fetch and process economic calendar data.
        :param save_sample: If True, save fetched HTML content to a file.
        :return: List of dictionaries containing event data filtered for US indices.
        """
        soup = self.fetch_html(save_sample)
        if not soup:
            return []

        table = soup.find('table', {"id": "economicCalendarData"})
        if not table:
            log_error("Economic calendar table not found.")
            return []

        rows = table.find_all('tr', {"class": "js-event-item"})
        return self.extract_data(rows)


    def save_html_to_file(self, html, file_path="sample/economic_calendar.html"):
        """
        Save HTML content to a file.
        :param html: The raw HTML content.
        :param file_path: Path to save the HTML file.
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, "wb") as file:
                file.write(html)
            print(f"HTML content saved to {file_path}")
        except Exception as e:
            log_error(f"Failed to save HTML content: {e}")

    def load_html_from_file(self, file_path):
        """
        Load and parse HTML content from a file.
        :param file_path: Path to the HTML file.
        :return: BeautifulSoup object or None if loading fails.
        """
        try:
            with open(file_path, "rb") as file:
                html = file.read()
            return BeautifulSoup(html, "html.parser")
        except Exception as e:
            log_error(f"Failed to load HTML from {file_path}: {e}")
            return None


    def read_data(self, file_path):
        """
        Read and parse HTML content from a file.
        :param file_path: Path to the HTML file.
        :return: BeautifulSoup object or None if loading fails.
        """
        try:
            # Load the sample HTML
            soup = self.load_html_from_file(file_path)
            if not soup:
                print("Failed to load or parse the sample HTML file.")
                return

            # Simulate the Fetcher processing the loaded HTML
            table = soup.find('table', {"id": "economicCalendarData"})
            if not table:
                print("Economic calendar table not found in the sample file.")
                return []

            # Extract rows from the table
            rows = table.find_all('tr', {"class": "js-event-item"})
            return self.extract_data(rows)

        except Exception as e:
            log_error(f"Failed to load HTML from {file_path}: {e}")
            return None

# Add __main__ function for standalone execution
if __name__ == "__main__":
    from config import Config
    base_url = Config.BASE_URL 
    fetcher = Fetcher(base_url) # Use default EST timezone
    print("Fetching data and saving to ./sample/economic_calendar.html...")
    fetcher.fetch_data(save_sample=True)
