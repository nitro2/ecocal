import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from utils import log_error


class Fetcher:
    def __init__(self, base_url):
        """
        Initialize Fetcher with the base URL.
        :param base_url: The URL of the economic calendar on Investing.com.
        """
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_data(self):
        """
        Fetch and parse economic calendar data.
        :return: List of dictionaries containing event data filtered for US indices.
        """
        try:
            req = urllib.request.Request(self.base_url, headers=self.headers)
            response = urllib.request.urlopen(req)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")

            # Locate and parse the economic calendar table
            table = soup.find('table', {"id": "economicCalendarData"})
            if not table:
                log_error("Economic calendar table not found.")
                return []

            rows = table.find_all('tr', {"class": "js-event-item"})
            return self._filter_us_data(rows)

        except HTTPError as e:
            log_error(f"HTTP Error: {e.code}")
        except Exception as e:
            log_error(f"Unexpected error: {e}")

        return []

    def _filter_us_data(self, rows):
        """
        Filter rows for US data (Currency: USD).
        :param rows: List of HTML rows from the economic calendar table.
        :return: List of dictionaries containing filtered US data.
        """
        filtered_data = []
        for row in rows:
            try:
                # Extract data
                currency = row.find('td', {"class": "flagCur"}).text.strip()
                if currency != "USD":
                    continue

                event = row.find('td', {"class": "event"}).text.strip()
                actual = row.find('td', {"class": "bold"}).text.strip()
                forecast = row.find('td', {"class": "fore"}).text.strip()
                previous = row.find('td', {"class": "prev"}).text.strip()

                # Append row data if all fields are present
                if actual and forecast and previous:
                    filtered_data.append({
                        "currency": currency,
                        "event": event,
                        "actual": self._parse_value(actual),
                        "forecast": self._parse_value(forecast),
                        "previous": self._parse_value(previous),
                    })
            except Exception as e:
                log_error(f"Error parsing row: {e}")

        return filtered_data

    def _parse_value(self, value):
        """
        Convert string values to appropriate numerical format.
        :param value: Raw value string from the table.
        :return: Parsed float or None if parsing fails.
        """
        try:
            return float(value.replace(',', '').replace('%', ''))
        except ValueError:
            return None
