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

    def _extract_data(self, rows):
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

    def fetch_data(self, save_sample=False):
        """
        Fetch and parse economic calendar data.
        :param save_sample: If True, save fetched HTML content to a file.
        :return: List of dictionaries containing event data filtered for US indices.
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
            table = soup.find('table', {"id": "economicCalendarData"})
            if not table:
                log_error("Economic calendar table not found.")
                return []

            rows = table.find_all('tr', {"class": "js-event-item"})
            return self._extract_data(rows)
        except HTTPError as e:
            log_error(f"HTTP Error: {e.code}")
        except Exception as e:
            log_error(f"Error fetching data: {e}")
        return []

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

# Add __main__ function for standalone execution
if __name__ == "__main__":
    from config import Config
    base_url = Config.BASE_URL 
    fetcher = Fetcher(base_url) # Use default EST timezone
    print("Fetching data and saving to ./sample/economic_calendar.html...")
    fetcher.fetch_data(save_sample=True)
