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

    def _convert_time(self, time_str, base_timezone="Etc/GMT+5"):
        """
        Convert a time string from the base timezone to the target timezone.
        :param time_str: Time string (e.g., "08:15").
        :param base_timezone: The base timezone of the time string.
        :return: Converted time string in the target timezone or None if parsing fails.
        """
        try:
            base_tz = timezone(base_timezone)
            target_tz = timezone(self.target_timezone)

            # Parse time string into a datetime object
            current_date = datetime.now().date()
            naive_time = datetime.strptime(time_str, "%H:%M")
            localized_time = base_tz.localize(datetime.combine(current_date, naive_time.time()))

            # Convert to the target timezone
            target_time = localized_time.astimezone(target_tz)
            return target_time.strftime("%H:%M")
        except Exception as e:
            log_error(f"Time conversion error: {e}")
            return None

    def _filter_us_data(self, rows):
        """
        Filter rows for US data (Currency: USD) and adjust timezones.
        :param rows: List of HTML rows from the economic calendar table.
        :return: List of dictionaries containing filtered US data with adjusted times.
        """
        filtered_data = []
        for row in rows:
            try:
                # Extract and convert time
                time_cell = row.find('td', {"class": "first left time"}) or row.find('td', {"class": "time"})
                raw_time = time_cell.text.strip() if time_cell else None
                time = self._convert_time(raw_time) if raw_time else "Unknown Time"

                # Extract currency
                currency_cell = row.find('td', {"class": "flagCur"})
                currency = currency_cell.text.strip() if currency_cell else None
                if currency != "USD":
                    continue

                # Extract event
                event_cell = row.find('td', {"class": "event"})
                event = event_cell.text.strip() if event_cell else "Unknown Event"

                # Extract actual, forecast, and previous values
                actual_cell = row.find('td', {"class": "bold"})
                forecast_cell = row.find('td', {"class": "fore"})
                previous_cell = row.find('td', {"class": "prev"})

                actual = self._parse_value(actual_cell.text.strip()) if actual_cell else None
                forecast = self._parse_value(forecast_cell.text.strip()) if forecast_cell else None
                previous = self._parse_value(previous_cell.text.strip()) if previous_cell else None

                # Append parsed data
                filtered_data.append({
                    "time": time,
                    "currency": currency,
                    "event": event,
                    "actual": actual,
                    "forecast": forecast,
                    "previous": previous,
                })
            except Exception as e:
                log_error(f"Error parsing row: {e}")

        return filtered_data

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
                self.save_html_to_file(html, file_path="sample/economic_calendar.html")

            soup = BeautifulSoup(html, "html.parser")
            table = soup.find('table', {"id": "economicCalendarData"})
            if not table:
                log_error("Economic calendar table not found.")
                return []

            rows = table.find_all('tr', {"class": "js-event-item"})
            return self._filter_us_data(rows)
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
    fetcher = Fetcher("https://www.investing.com/economic-calendar/")
    print("Fetching data and saving to ./sample/economic_calendar.html...")
    fetcher.fetch_data(save_sample=True)
