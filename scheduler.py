import schedule
import time
from config import Config

class Scheduler:
    def __init__(self):
        pass

    def schedule_tasks(self, task_function):
        """
        Schedule tasks for periodic execution based on SCHEDULE_INTERVAL and CRITICAL_TIMES in Config.
        :param task_function: The function to execute for each scheduled task.
        """
        # Schedule based on SCHEDULE_INTERVAL
        interval = Config.INTERVAL_VALUE
        unit = Config.INTERVAL_UNIT

        if unit == "seconds":
            print(f"Task scheduled to run every {interval} seconds.")
            schedule.every(interval).seconds.do(task_function)
        elif unit == "minutes":
            schedule.every(interval).minutes.do(task_function)
            print(f"Task scheduled to run every {interval} minutes.")
        elif unit == "hours":
            schedule.every(interval).hours.do(task_function)
            print(f"Task scheduled to run every {interval} hours.")
        elif unit == "days":
            schedule.every(interval).days.at("00:00").do(task_function)
            print(f"Task scheduled to run every {interval} days.")
        else:
            print("Unknown schedule interval unit. Defaulting to every minute.")
            schedule.every(1).minutes.do(task_function)

        # Schedule tasks for the configured critical times
        for critical_time in Config.CRITICAL_TIMES:
            day = critical_time["day"]
            time_str = critical_time["time"]
            getattr(schedule.every(), day).at(time_str).do(task_function)
            print(f"Task scheduled for {day} at {time_str}.")

    def run_forever(self):
        """
        Runs the scheduled tasks indefinitely.
        """
        print("Running scheduled tasks...")
        if Config.INTERVAL_UNIT == "seconds":
            while True:
                print("INTERVAL_UNIT1")
                schedule.run_pending()
                print("INTERVAL_UNIT2")
                time.sleep(Config.INTERVAL_VALUE)
        else:
            while True:
                schedule.run_pending()
                time.sleep(1)
