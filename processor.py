from enum import Enum
from utils import prettify_rows

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

    def classify_signal(self, actual, forecast, previous):
        """
        Classify signal based on Actual, Forecast, and Previous values.
        :param actual: The actual value of the event.
        :param forecast: The forecast value of the event.
        :param previous: The previous value of the event.
        :return: A SignalLevel representing the signal.
        """
        if actual is None or forecast is None or previous is None:
            return SignalLevel.NO_SIGNAL  # Handle missing values gracefully

        if actual > forecast and actual > previous:
            return SignalLevel.STRONG_BUY
        elif actual > forecast:
            return SignalLevel.BUY
        elif actual < forecast and actual < previous:
            return SignalLevel.STRONG_SELL
        elif actual < forecast:
            return SignalLevel.SELL
        else:
            return SignalLevel.NEUTRAL

    def aggregate_signals(self, rows):
        """
        Aggregate signals for multiple events at the same time.
        :param rows: List of rows with signal data.
        :return: The overall signal for all rows.
        """
        signals = [self.classify_signal(row['actual'], row['forecast'], row['previous']) for row in rows]

        # Print prettified rows with signals
        prettify_rows(rows, signals)

        # Aggregate by counting occurrences of each signal
        signal_counts = {signal: signals.count(signal) for signal in set(signals)}
        most_common_signal = max(signal_counts, key=signal_counts.get)
        
        return most_common_signal
