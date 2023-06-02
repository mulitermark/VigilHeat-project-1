import datetime
import io
import random
from collections import Counter
import string
import cv2
import matplotlib.pyplot as plt
import numpy as np


class HistogramGenerator:
    def __init__(self, interval):
        plt.switch_backend("agg")
        self.interval = interval
        self.hourly_count = Counter()
        self.minute_count = Counter()
        self.minute_fps = Counter()
        self.hourly_fps = Counter()
        self.counter = 0
        self.histogram_image = self.generate_histogram()

    def process_input(self, n_detections, timestamp):
        """
        This method processes the timestamp and increments the count in the corresponding time intervals.
        """
        hour = timestamp.hour
        minute = timestamp.minute

        self.hourly_count[hour] += n_detections
        self.minute_count[minute] += n_detections
        self.minute_fps[minute] += 1
        self.hourly_fps[hour] += 1

    def add_input(self, detection_list, timestamp=None):
        """
        This method adds a list of timestamps to the histogram.
        """
        if timestamp is None:
            # use now as timestamp
            timestamp = datetime.datetime.now()
        if detection_list is None:
            return
        print(detection_list)
        n_detections = len(detection_list)
        if n_detections > 0:
            self.process_input(n_detections, timestamp)

        self.counter += 1
        if self.counter >= 20:
            print("Generating histogram")
            self.counter = 0
            self.histogram_image = self.generate_histogram()

    def generate_histogram(self, start=0, end=59):
        """
        This method generates a histogram based on the interval and range provided.
        """
        if self.interval == "hour":
            data = self.hourly_count
            data_fps = self.hourly_fps
            # calculate the upper round int average number of detections per hour
            data = {key: round(value / data_fps[key], 0) for key, value in data.items()}
            xlabel = "Hour of the day"
            x = list(range(start, end + 1))
            x_labels = x
        elif self.interval == "minute":
            data = self.minute_count
            data_fps = self.minute_fps
            # calculate the int average number of detections per minute
            data = {key: round(value / data_fps[key], 0) for key, value in data.items()}
            xlabel = "Minute of the hour"
            x = list(range(start, end + 1))
            x_labels = [f"{minute:02d}" if minute % 5 == 0 else "" for minute in x]
        else:
            raise ValueError("Invalid interval. Choose from 'hour' or 'minute'.")

        counts = [data.get(key, 0) for key in x]
        # blue color for the bars
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.bar(x, counts, color="#1f77b4")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Number of detections")
        ax.set_title(
            f"Person detection count per {self.interval} from {start} to {end}"
        )
        ax.set_xticks(x, x_labels, rotation=45)

        # Return the histogram image as a cv2 image
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))[:, :, ::-1]
        plt.close(fig)
        return image


# Test data generator
def generate_test_data(n_samples=3000, n_detections=30):
    return [
        random.choices(string.ascii_letters, k=n_detections) for _ in range(n_samples)
    ]


# Test cases
def test_generate_histogram():
    histogram = HistogramGenerator("minute")
    test_data = generate_test_data()
    now = datetime.datetime.now()
    for data in test_data:
        histogram.add_input(data, timestamp=now)
        now += datetime.timedelta(seconds=(1 / 30))
        # plot the histogram
        cv2.imshow("Histogram", histogram.histogram_image)
        cv2.waitKey(1)


# if __name__ == "__main__":
#     test_generate_histogram()
