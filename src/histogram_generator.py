import datetime
import io
import random
from collections import defaultdict
import cv2
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
import numpy as np

class HistogramGenerator:
    def __init__(self, interval):
        self.interval = interval
        self.hourly_count = defaultdict(int)
        self.daily_count = defaultdict(lambda: [datetime.date(2023, 1, 1), 0])
        self.weekly_count = defaultdict(lambda: defaultdict(int))
        self.minute_count = defaultdict(int)

    def process_input(self, timestamp):
        """
        This method processes the timestamp and increments the count in the corresponding time intervals.
        """
        week_number = timestamp.isocalendar()[1]
        day_of_year = timestamp.timetuple().tm_yday
        hour = timestamp.hour
        minute = timestamp.minute
        day_of_week = timestamp.weekday()

        self.hourly_count[hour] += 1
        self.daily_count[day_of_year][1] += 1
        self.weekly_count[week_number][day_of_week] += 1
        self.minute_count[minute] += 1

    def add_input(self, detection_list, timestamp = None):
        """
        This method adds a list of timestamps to the histogram.
        """
        if timestamp is None:
            # use now as timestamp
            timestamp = datetime.datetime.now()

        for _ in detection_list:
            self.process_input(timestamp)

        return self.generate_histogram()

    def generate_histogram(self, start=0, end=59):
        """
        This method generates a histogram based on the interval and range provided.
        """
        if self.interval == 'hour':
            data = self.hourly_count
            xlabel = 'Hour of the day'
            x = list(range(start, end + 1))
            x_labels = x

        elif self.interval == 'day':
            data = {day: count for day, (_, count) in self.daily_count.items()}
            xlabel = 'Day of the year'
            x = list(range(start, end + 1))
            x_labels = [datetime.datetime.now() + datetime.timedelta(days=day - 1) for day in x]
            x_labels = [date.strftime('%b %d') for date in x_labels]

        elif self.interval == 'week':
            data = {week: sum(counts.values()) for week, counts in self.weekly_count.items()}
            xlabel = 'Week of the year'
            x = list(range(start, end + 1))
            x_labels = [f"Week {i}" for i in x]

        elif self.interval == 'minute':
            data = self.minute_count
            xlabel = 'Minute of the hour'
            x = list(range(start, end + 1))
            x_labels = [f'{minute:02d}' if minute % 5 == 0 else '' for minute in x]
        else:
            raise ValueError("Invalid interval. Choose from 'hour', 'day', 'week', or 'minute'.")

        counts = [data.get(key, 0) for key in x]
        # blue color for the bars
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.bar(x, counts, color='#1f77b4')
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Number of detections")
        ax.set_title(f"Person detection count per {self.interval} from {start} to {end}")
        ax.set_xticks(x, x_labels, rotation=45)

        # Return the histogram image as a cv2 image
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))[:, :, ::-1]
        plt.close(fig)
        return image

# Test data generator
def generate_test_data(months=0, days=0, hours=0, minutes=0):
    current_time = datetime.datetime.now()
    test_data = []

    for _ in range(1000):
        random_time = current_time + relativedelta(
            months=random.randint(0, months),
            days=random.randint(0, days),
            hours=random.randint(0, hours),
            minutes=random.randint(0, minutes),
            seconds=random.randint(0, 59)
        )
        test_data.append(random_time)

    return test_data



# Test cases
def test_generate_histogram():

    histogram = HistogramGenerator('minute')
    test_data = generate_test_data(minutes=60)
    histogram.add_input(test_data)
    histogram.generate_histogram(0, 59)   # Minute histogram

    histogram = HistogramGenerator('hour')
    test_data = generate_test_data(hours=24)
    histogram.add_input(test_data)
    histogram.generate_histogram(0, 23)   # Hourly histogram

    histogram = HistogramGenerator('day')
    test_data = generate_test_data(days=7)
    histogram.add_input(test_data)
    histogram.generate_histogram(1, 30)   # Daily histogram

    histogram = HistogramGenerator('week')
    test_data = generate_test_data(months=3)
    histogram.add_input(test_data)
    histogram.generate_histogram(1, 50)   # Weekly histogram
