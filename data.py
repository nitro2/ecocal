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
    def __init__(self, id: str, actual: Value, previous:Value , forecast: Value, pn_indicator: str):
        self.id = id
        self.actual = actual.value if actual else None
        self.previous = previous.value if previous else None
        self.forecast = forecast.value if forecast else None
        self.pn_indicator = pn_indicator
        self.signal = self.classify_signal()

    def __str__(self):
        return f"Id: {self.id}  Actual: {self.actual}, Previous: {self.previous}, Forecast: {self.forecast}, PN Indicator: {self.pn_indicator}"

    def __repr__(self):
        return self.__str__()
    
    def classify_signal(self):
        """
        Classify the signal based on actual, forecast, and previous values, considering P/N indicator.
        :return: Signal classification as a string
        """
        # Ensure all required values are present
        if self.previous is None:
            return SignalLevel.NEUTRAL.value

        try:
            # Calculate changes relative to previous
            delta_prev = (self.actual - self.previous) / self.previous if self.previous != 0 else 0
            delta_forecast = None
            if self.forecast is not None:
                if self.actual != self.previous:
                    delta_forecast = (self.actual - self.forecast) / (self.actual - self.previous) if self.previous != 0 else 0
                else:
                    delta_forecast = (self.actual - self.forecast) / (self.actual) if self.actual != 0 else 0
            # print(f"Id: {self.id} - Delta forecast: {delta_forecast} - Delta previous: {delta_prev}")

            # Determine the signal based on conditions
            if self.forecast is None:  # No forecast case
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
                if self.forecast > self.previous:  # Forecast is higher than previous
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
                elif self.forecast < self.previous < self.actual:  # Actual exceeds both forecast and previous
                    signal = SignalLevel.STRONG_BUY.value
                elif self.forecast > self.previous > self.actual:  # Actual falls below both forecast and previous
                    signal = SignalLevel.STRONG_SELL.value
                else:
                    signal = SignalLevel.NEUTRAL.value

            # Adjust for P/N indicator
            if self.pn_indicator == "Negative":
                if SignalLevel.BUY.value in signal:
                    signal = signal.replace(SignalLevel.BUY.value, SignalLevel.SELL.value)
                elif SignalLevel.SELL.value in signal:
                    signal = signal.replace(SignalLevel.SELL.value, SignalLevel.BUY.value)

            return signal
        except Exception as e:
            print(f"Error classifying signal: {e}")
            print(f"Id: {self.id}, Actual: {self.actual}, Forecast: {self.forecast}, Previous: {self.previous}")
            return SignalLevel.NO_SIGNAL.value