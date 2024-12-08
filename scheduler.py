import time
from datetime import datetime, timedelta
from threading import Thread
from config import Config


class Scheduler:
    def __init__(self, task_function):
        """
        Initialize the Scheduler with a task function and interval configurations.
        :param task_function: The function to execute at intervals.
        """
        self.task_function = task_function
        self.default_interval = Config.DEFAULT_INTERVAL_VALUE
        self.default_unit = Config.DEFAULT_INTERVAL_UNIT
        self.critical_interval = Config.CRITICAL_INTERVAL_VALUE
        self.critical_unit = Config.CRITICAL_INTERVAL_UNIT
        self.running = False

    def get_interval_in_seconds(self, interval_value, interval_unit):
        """
        Convert interval value and unit to seconds.
        :param interval_value: The interval value (e.g., 10).
        :param interval_unit: The interval unit (e.g., 'seconds').
        :return: Interval in seconds.
        """
        if interval_unit == "seconds":
            return interval_value
        elif interval_unit == "minutes":
            return interval_value * 60
        return 10  # Default fallback to 10 seconds if invalid

    def is_critical_time(self):
        """
        Check if the current time is within 1 minute of any critical time (H:M:S format).
        :return: True if in critical time, False otherwise.
        """
        now = datetime.now()
        for critical in Config.CRITICAL_TIMES:
            critical_time = datetime.strptime(critical["time"], "%H:%M:%S").replace(
                year=now.year, month=now.month, day=now.day
            )
            # Allow a 1-minute window
            if critical_time <= now < critical_time + timedelta(minutes=1):
                return True
        return False

    def get_current_interval(self):
        """
        Get the current interval in seconds based on whether it's critical time.
        :return: Interval in seconds.
        """
        if self.is_critical_time():
            return self.get_interval_in_seconds(self.critical_interval, self.critical_unit)
        return self.get_interval_in_seconds(self.default_interval, self.default_unit)

    def start(self):
        """
        Start the scheduler.
        """
        self.running = True
        while self.running:
            current_interval = self.get_current_interval()
            print(f"Running task... (Interval: {current_interval}s)")
            self.task_function()
            time.sleep(current_interval)

    def stop(self):
        """
        Stop the scheduler.
        """
        self.running = False
