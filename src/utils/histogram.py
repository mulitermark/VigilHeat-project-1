
import datetime
import random
from collections import defaultdict
import matplotlib.pyplot as plt

def process_input(timestamp):
    """
    This function processes the timestamp and increments the count in the corresponding time intervals.
    """
    week_number = timestamp.isocalendar()[1]
    day_of_year = timestamp.timetuple().tm_yday
    hour = timestamp.hour
    day_of_week = timestamp.weekday()

    hourly_count[hour] += 1
    daily_count[day_of_year][1] += 1
    weekly_count[week_number][day_of_week] += 1

def generate_histogram(interval, start, end):
    """
    This function generates a histogram based on the interval and range provided.
    """
    if interval == 'hour':
        data = hourly_count
        xlabel = 'Hour of the day'
        x = list(range(start, end + 1))
        x_labels = x
    elif interval == 'day':
        data = {day: count for day, (_, count) in daily_count.items()}
        xlabel = 'Day of the year'
        x = list(range(start, end + 1))
        x_labels = [datetime.datetime(2023, 1, 1) + datetime.timedelta(days=day - 1) for day in x]
        x_labels = [date.strftime('%b %d') for date in x_labels]
    elif interval == 'week':
        data = {week: sum(counts.values()) for week, counts in weekly_count.items()}
        xlabel = 'Week of the year'
        x = list(range(start, end + 1))
        x_labels = [f"Week {i}" for i in x]
    else:
        raise ValueError("Invalid interval. Choose from 'hour', 'day', or 'week'.")

    counts = [data.get(key, 0) for key in x]

    plt.bar(x, counts)
    plt.xlabel(xlabel)
    plt.ylabel("Number of people")
    plt.title(f"People count per {interval} from {start} to {end}")
    plt.xticks(x, x_labels, rotation=45)
    plt.show()


# Test data generator
def generate_test_data():
    test_data = []

    for _ in range(1000):
        test_data.append(datetime.datetime(2023, random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)))

    return test_data

# Test cases
def test_generate_histogram():
    test_data = generate_test_data()

    for timestamp in test_data:
        process_input(timestamp)

    # Test different intervals and ranges
    generate_histogram('hour', 0, 23)   # Hourly histogram
    generate_histogram('day', 1, 7)   # Daily histogram
    generate_histogram('week', 8, 12)   # Weekly histogram

if __name__ == "__main__":
    hourly_count = defaultdict(int)
    daily_count = daily_count = defaultdict(lambda: [datetime.date(2023, 1, 1), 0])
    weekly_count = defaultdict(lambda: defaultdict(int))

    test_generate_histogram()