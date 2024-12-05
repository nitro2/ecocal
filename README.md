# **US Index Signal Generator**

This project fetches economic calendar data from Investing.com and processes US index data to generate Buy/Sell signals based on `Actual`, `Forecast`, and `Previous` values. The tool helps investors make informed decisions by providing individual and aggregate signals.

## **Project Structure**

```plaintext
project/
│
├── fetcher.py          # Fetches and filters economic calendar data for US indexes.
├── processor.py        # Processes data to classify Buy/Sell signals.
├── scheduler.py        # Manages periodic and critical-time execution of tasks.
├── config.py           # Configuration settings, such as URLs and schedules.
├── utils.py            # Shared utility functions, such as logging and parsing.
├── main.py             # Entry point of the application.
│
└── test/               # Contains test scripts for individual modules.
    └── test_fetcher.py # Tests data fetching and filtering functionality.
```

## **Modules Overview**

### 1. **`fetcher.py`**
- **Purpose**: Fetches and filters US-specific economic data from Investing.com.
- **Key Responsibilities**:
  - Fetch raw HTML data from the economic calendar.
  - Parse and filter rows where the currency is `USD`.
  - Handle missing or malformed data gracefully.
- **Key Methods**:
  - `fetch_data()`: Retrieves and parses economic calendar data.
  - `_filter_us_data(rows)`: Filters rows for US-specific events.
  - `_parse_value(value)`: Converts string values to numerical format (e.g., `6.3%` → `6.3`).

### 2. **`processor.py`**
- **Purpose**: Processes fetched data and classifies Buy/Sell signals.
- **Key Responsibilities**:
  - Classify individual signals using the `Actual`, `Forecast`, and `Previous` values.
  - Generate an aggregate signal for events occurring at the same time.
- **Key Methods**:
  - `classify_signal(actual, forecast, previous)`: Returns signal levels (e.g., `Strong Buy`, `Neutral`).
  - `aggregate_signals(rows)`: Computes an overall signal for overlapping events.

### 3. **`scheduler.py`**
- **Purpose**: Manages the periodic execution of tasks.
- **Key Responsibilities**:
  - Run tasks hourly or at critical times (e.g., every 2 seconds at 22:00 on Wednesdays).
- **Key Methods**:
  - `schedule_tasks(task_function)`: Configures the task schedule.
  - `run_forever()`: Starts the scheduler loop.

### 4. **`config.py`**
- **Purpose**: Stores project configurations.
- **Contents**:
  - Base URL for the Investing.com economic calendar.
  - Critical execution times (e.g., `22:00 on Wednesdays`).

### 5. **`utils.py`**
- **Purpose**: Provides reusable utility functions.
- **Key Functions**:
  - `log_error(message)`: Logs error messages with timestamps.
  - `log_info(message)`: Logs informational messages.
  - `parse_time(time_str)`: Parses string times into `datetime` objects.

### 6. **`main.py`**
- **Purpose**: Integrates all modules and acts as the entry point for the program.
- **Workflow**:
  1. Fetch data using `Fetcher`.
  2. Process data using `SignalProcessor`.
  3. Schedule periodic execution using `Scheduler`.

## **How to Run**

### Prerequisites
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Setup .env file
Copy .env.example to .env
```bash
cp .env.example .env
```

### Steps
Execute the main script:

```bash
python main.py
```

Run individual tests (e.g., for fetcher.py):

```bash
python test/test_fetcher.py
```

## **Future Enhancements**
- Integration with trading APIs for automated orders.
- Enhanced classification formula for Buy/Sell signals.
- Real-time alerts via email or SMS.
- Extended support for other currencies or regions.






