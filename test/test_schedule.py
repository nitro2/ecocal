import time
from datetime import datetime, timedelta
from threading import Thread
from scheduler import Scheduler
from config import Config


def mock_task():
    """
    A mock task function to simulate task execution.
    Prints a timestamp for testing.
    """
    print(f"Task executed at {datetime.now().strftime('%H:%M:%S')}")

def test_scheduler():
    """
    Test the Scheduler to verify correct intervals for normal and critical times.
    """
    # Set test configuration
    Config.SCHEDULE_INTERVAL_DEFAULT = "5s"  # Default interval for testing
    Config.SCHEDULE_INTERVAL_CRITICAL = "2s"  # Critical interval for testing

    # Mock critical time as 10 seconds from now
    now = datetime.now()
    critical_time = (now + timedelta(seconds=10)).strftime("%H:%M:%S")
    Config.CRITICAL_TIMES = [{"day": now.strftime("%A").lower(), "time": critical_time}]

    # Initialize the scheduler with the mock task
    scheduler = Scheduler(mock_task)

    # Run the scheduler in a separate thread
    def run_scheduler():
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.stop()

    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()

    # Run the test for 20 seconds
    time.sleep(20)
    scheduler.stop()
    scheduler_thread.join()


if __name__ == "__main__":
    test_scheduler()
