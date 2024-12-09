from fetcher import Fetcher
from processor import SignalProcessor
from scheduler import Scheduler
from config import Config
from datetime import datetime

def run_task():
    """
    Defines the task to fetch and process data, then output the result.
    """
    print(f"[{datetime.now()}] Running task...")  # Add timestamp
    fetcher = Fetcher(Config.BASE_URL, target_timezone=Config.TARGET_TIMEZONE)
    processor = SignalProcessor()

    dataset = fetcher.fetch_data()
    if dataset:
        # Aggregate and classify signals for the data
        overall_signal = processor.aggregate_signals(dataset)
        print(f"Overall Signal: {overall_signal}")
    else:
        print("No data fetched.")

    print("Task complete.\n"+'-'*50)

if __name__ == "__main__":
    scheduler = Scheduler(run_task)
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.stop()
