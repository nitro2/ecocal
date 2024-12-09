from utils import prettify_dataset
from json import load
from data import Data, SignalLevel

# Load positivity mapping once at the top
with open("event_data.json", "r") as f:
    event_data_json = load(f)


class SignalProcessor:
    def __init__(self):
        pass

    def aggregate_signals(self, dataset):
        """
        Aggregate signals for multiple events at the same time.
        :param dataset: List of dataset with signal data.
        :return: The overall signal for all dataset.
        """
        # Add Positive/Negative indicator to each d
        dataset = self.add_pn_indicator(dataset)
        signals = [self.classify_signal(d) for d in dataset]

        # Print prettified dataset with signals
        prettify_dataset(dataset)

        # Aggregate by counting occurrences of each signal
        signal_counts = {signal: signals.count(signal) for signal in set(signals)}
        most_common_signal = max(signal_counts, key=signal_counts.get)

        return most_common_signal

    def add_pn_indicator(self, dataset):
        """
        Add Positive/Negative (P/N) indicator to each d based on the event name.
        :param dataset: List of dictionaries containing d data.
        :return: List of dataset with 'pn_indicator' field added.
        """
        for d in dataset:
            # Match the event name to the positivity mapping
            pn = event_data_json.get(d.id)
            pn_indicator = pn.get("pn_indicator").lower() if pn else None
            d.set_pn_indicator(pn_indicator)
        return dataset
    
    def classify_signal(self, d: Data):
        """
        Classify the signal based on actual, forecast, and previous values, considering P/N indicator.
        :return: Signal classification as a string
        """
        actual = d.actual.value if d.actual else None
        forecast = d.forecast.value if d.forecast else None
        previous = d.previous.value if d.previous else None
        pn_indicator = d.pn_indicator

        try:
            # Ensure all required values are present
            if previous is None:
                signal = SignalLevel.NEUTRAL.value
                return signal
            if actual is None:
                signal = SignalLevel.NO_SIGNAL.value
                return signal

            # Calculate changes relative to previous
            delta_prev = (actual - previous) / previous if previous != 0 else 0
            delta_forecast = None
            if forecast is not None:
                if actual != previous:
                    delta_forecast = (actual - forecast) / (actual - previous) if previous != 0 else 0
                else:
                    delta_forecast = (actual - forecast) / (actual) if actual != 0 else 0
            # print(f"Id: {id} - Delta forecast: {delta_forecast} - Delta previous: {delta_prev}")

            # Determine the signal based on conditions
            if forecast is None:  # No forecast case
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
                if forecast > previous:  # Forecast is higher than previous
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
                elif forecast < previous < actual:  # Actual exceeds both forecast and previous
                    signal = SignalLevel.STRONG_BUY.value
                elif forecast > previous > actual:  # Actual falls below both forecast and previous
                    signal = SignalLevel.STRONG_SELL.value
                else:
                    signal = SignalLevel.NEUTRAL.value

            # Adjust for P/N indicator
            if pn_indicator == "negative":
                if SignalLevel.BUY.value in signal:
                    signal = signal.replace(SignalLevel.BUY.value, SignalLevel.SELL.value)
                elif SignalLevel.SELL.value in signal:
                    signal = signal.replace(SignalLevel.SELL.value, SignalLevel.BUY.value)

            return signal
        except Exception as e:
            print(f"Error classifying signal: {e}")
            print(f"Id: {d.id}, Actual: {d.actual}, Forecast: {d.forecast}, Previous: {d.previous}")
            return SignalLevel.NO_SIGNAL.value
        finally:
            d.set_signal(signal)
