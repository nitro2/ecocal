from enum import Enum
from utils import prettify_rows
from json import load

# Load positivity mapping once at the top
with open("positivity_mapping.json", "r") as f:
    positivity_mapping = load(f)

class SignalLevel(Enum):
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    WEAK_BUY = "Weak Buy"
    NEUTRAL = "Neutral"
    WEAK_SELL = "Weak Sell"
    SELL = "Sell"
    STRONG_SELL = "Strong Sell"
    NO_SIGNAL = "No Signal"

class SignalProcessor:
    def __init__(self):
        pass

    def classify_signal(self, actual, forecast, previous, pn_indicator=None):
        """
        Classify the signal based on actual, forecast, and previous values, considering P/N indicator.
        :param actual: Value object or None
        :param forecast: Value object or None
        :param previous: Value object or None
        :param pn_indicator: 'Positive', 'Negative', or None
        :return: Signal classification as a string
        """
        # Extract numerical values from Value objects or default to None
        actual_val = actual.value if actual else None
        forecast_val = forecast.value if forecast else None
        previous_val = previous.value if previous else None

        # Ensure all required values are present
        if actual_val is None or previous_val is None:
            return SignalLevel.NEUTRAL.value

        try:
            # Calculate changes relative to previous
            delta_prev = (actual_val - previous_val) / previous_val if previous_val != 0 else 0
            delta_forecast = None
            if forecast_val is not None:
                if actual_val != previous_val:
                    delta_forecast = (actual_val - forecast_val) / (actual_val - previous_val) if previous_val != 0 else 0
                else:
                    delta_forecast = (actual_val - forecast_val) / (actual_val) if actual_val != 0 else 0

            # Determine the signal based on conditions
            if forecast_val is None:  # No forecast case
                if delta_prev > 0.2:
                    signal = SignalLevel.STRONG_BUY.value
                elif delta_prev > 0.1:
                    signal = SignalLevel.BUY.value
                elif delta_prev < -0.2:
                    signal = SignalLevel.STRONG_SELL.value
                elif delta_prev < -0.1:
                    signal = SignalLevel.SELL.value
                else:
                    signal = SignalLevel.NEUTRAL.value
            else:  # Forecast provided case
                if forecast_val > previous_val:  # Forecast is higher than previous
                    if delta_forecast > 0.2:
                        signal = SignalLevel.STRONG_BUY.value
                    elif delta_forecast > 0.1:
                        signal = SignalLevel.BUY.value
                    elif delta_forecast < -0.2:
                        signal = SignalLevel.STRONG_SELL.value
                    elif delta_forecast < -0.1:
                        signal = SignalLevel.SELL.value
                    else:
                        signal = SignalLevel.NEUTRAL.value
                elif forecast_val < previous_val < actual_val:  # Actual exceeds both forecast and previous
                    signal = SignalLevel.STRONG_BUY.value
                elif forecast_val > previous_val > actual_val:  # Actual falls below both forecast and previous
                    signal = SignalLevel.STRONG_SELL.value
                else:
                    signal = SignalLevel.NEUTRAL.value

            # Adjust for P/N indicator
            if pn_indicator == "Negative":
                if SignalLevel.BUY.value in signal:
                    signal = signal.replace(SignalLevel.BUY.value, SignalLevel.SELL.value)
                elif SignalLevel.SELL.value in signal:
                    signal = signal.replace(SignalLevel.SELL.value, SignalLevel.BUY.value)

            return signal
        except Exception as e:
            print(f"Error classifying signal: {e}")
            print(f"Actual: {actual_val}, Forecast: {forecast_val}, Previous: {previous_val}")
            return SignalLevel.NO_SIGNAL.value

    def aggregate_signals(self, rows):
        """
        Aggregate signals for multiple events at the same time.
        :param rows: List of rows with signal data.
        :return: The overall signal for all rows.
        """
        # Add Positive/Negative indicator to each row
        rows = self.add_pn_indicator(rows)

        # Classify signals for each row
        signals = [self.classify_signal(row['actual'], row['forecast'], row['previous'], row['pn_indicator']) for row in rows]

        # Print prettified rows with signals
        prettify_rows(rows, signals)

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
            event_name = row.get("event", "_").split("(")[0].strip()
            # Match the event name to the positivity mapping
            row["pn_indicator"] = positivity_mapping.get(event_name, "_")  # Default to "_"
        return rows