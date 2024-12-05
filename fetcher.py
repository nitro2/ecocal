import os
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

    def _filter_us_data(self, rows):
        """
        Dummy method for now. Replace this with actual filtering logic.
        """
        return []

# Add __main__ function for standalone execution
if __name__ == "__main__":
    fetcher = Fetcher("https://www.investing.com/economic-calendar/")
    print("Fetching data and saving to ./sample/economic_calendar.html...")
    fetcher.fetch_data(save_sample=True)
