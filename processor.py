from utils import prettify_rows
from json import load
from data import Data

# Load positivity mapping once at the top
with open("event_data.json", "r") as f:
    event_data_json = load(f)


class SignalProcessor:
    def __init__(self):
        pass

    def aggregate_signals(self, rows):
        """
        Aggregate signals for multiple events at the same time.
        :param rows: List of rows with signal data.
        :return: The overall signal for all rows.
        """
        # Add Positive/Negative indicator to each row
        rows = self.add_pn_indicator(rows)

        # Classify signals for each row
        for row in rows:
            d = Data(row['id'], row['actual'], row['previous'], row['forecast'], row['pn_indicator'])
            row['signal'] = d.classify_signal()
        signals = [row['signal'] for row in rows]

        # Print prettified rows with signals
        prettify_rows(rows)

        # Aggregate by counting occurrences of each signal
        signal_counts = {signal: signals.count(signal) for signal in set(signals)}
        most_common_signal = max(signal_counts, key=signal_counts.get)

        return most_common_signal

    def add_pn_indicator(self, rows):
        """
        Add Positive/Negative (P/N) indicator to each row based on the event name.
        :param rows: List of dictionaries containing row data.
        :return: List of rows with 'pn_indicator' field added.
        """
        for row in rows:
            # Extract the base event name by removing parentheses and trimming whitespace
            id = row.get("id", "")
            # Match the event name to the positivity mapping
            row["pn_indicator"] = event_data_json.get(id, "_").get("pn_indicator")  # Default to "_"
        return rows