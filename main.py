from fetcher import Fetcher
from processor import SignalProcessor
from scheduler import Scheduler
from config import Config

def main():
    try:
        # Initialize components
        fetcher = Fetcher(Config.BASE_URL)
        processor = SignalProcessor()
        scheduler = Scheduler()

        # Define the main task
        def run_task():
            print("Fetching data...")
            data = fetcher.fetch_data()

            if not data:
                print("No data available or an error occurred.")
                return

            print("Processing signals...")
            for row in data:
                # Per-row signal processing
                row_signal = processor.classify_signal(row['actual'], row['forecast'], row['previous'])
                print(f"Event: {row['event']} -> Signal: {row_signal}")

            # Aggregate signals for overlapping events
            overall_signal = processor.aggregate_signals(data)
            print(f"Overall Signal: {overall_signal}")

        # Schedule tasks
        scheduler.schedule_tasks(run_task)
        scheduler.run_forever()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
