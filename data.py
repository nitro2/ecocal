from enum import Enum

class SignalLevel(Enum):
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    WEAK_BUY = "Weak Buy"
    NEUTRAL = "Neutral"
    WEAK_SELL = "Weak Sell"
    SELL = "Sell"
    STRONG_SELL = "Strong Sell"
    NO_SIGNAL = "No Signal"

class Value:
    def __init__(self, value, unit, color):
        """
        Represents a value with an associated color (e.g., redFont, greenFont).
        :param value: The numerical or string value.
        :param unit: The unit of the value (e.g., '%', 'k').
        :param color: The associated color as a string (e.g., 'red', 'green').
        """
        self.value = value
        self.unit = unit
        self.color = color

    def __repr__(self):
        return f"Value(value={self.value}, color={self.color})"

# Data class contains the actual, previous, forecast values and pn_indicator for a given currency
class Data:
    def __init__(self, time: str, currency: str, event: str, id: str, importance: int,
                 actual: Value, previous: Value, forecast: Value):
        self.time = time
        self.currency = currency
        self.event = event
        self.id = id
        self.importance = importance
        self.event = event
        self.actual = actual
        self.previous = previous
        self.forecast = forecast
        self.pn_indicator = ""

        self.signal = None

    def __str__(self):
        return f"Id: {self.id}  Actual: {self.actual}, Previous: {self.previous}, Forecast: {self.forecast}, PN Indicator: {self.pn_indicator}"

    def __repr__(self):
        return self.__str__()
    
    def set_pn_indicator(self, pn_indicator):
        """
        Set the Positive/Negative indicator for the data.
        :param pn_indicator: The Positive/Negative indicator as a string.
        """
        self.pn_indicator = pn_indicator

    def set_signal(self, signal):
        """
        Set the signal for the data.
        :param signal: The signal as a string.
        """
        self.signal = signal