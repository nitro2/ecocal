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
    run_task()  # Run the task once before scheduling
    scheduler.schedule_tasks(run_task)  # Pass the task function to the scheduler
    scheduler.run_forever()
