from fetcher import Fetcher
from processor import SignalProcessor
from scheduler import Scheduler
from config import Config

def run_task():
    """
    Defines the task to fetch and process data, then output the result.
    """
    fetcher = Fetcher(target_timezone=Config.TARGET_TIMEZONE)
    processor = SignalProcessor()

    print("Running task...")
    data = fetcher.fetch_data()
    if data:
        # Aggregate and classify signals for the data
        overall_signal = processor.aggregate_signals(data)
        print(f"Overall Signal: {overall_signal}")
    else:
        print("No data fetched.")

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.schedule_tasks(run_task)  # Pass the task function to the scheduler
    scheduler.run_forever()
