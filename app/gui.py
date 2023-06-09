import datetime
import sys
import cv2
import numpy as np
import time
import threading

from person_detector import PersonDetector
from heatmap_generator import HeatmapGenerator
from stream_handler import VideoStreamHandler
from histogram_generator import HistogramGenerator

FPS = 12
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
CAM_WIDTH = 1280
CAM_HEIGHT = 720

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

YOUR_EMAIL = "your_email@gmail.com"  # replace with your Gmail address
YOUR_PASSWORD = "your_password"  # replace with your Gmail password


class Application:
    def __init__(self, video_path, queue_sector=None):
        self.updating = True
        self.frame = None
        self.heatmap = None
        self.histogram = None
        self.queue_sector = queue_sector
        self.queue = 0
        self.prev_queue = 0
        self.queue_limit = 3
        self.time_last_warning = datetime.datetime.now() - datetime.timedelta(minutes=5)

        self.heatmap_generator = HeatmapGenerator(CAM_WIDTH, CAM_HEIGHT)
        self.histogram_generator = HistogramGenerator("minute")

        video_path = check_and_resize_video(video_path)
        self.streamer = VideoStreamHandler(video_path)
        self.person_detector = PersonDetector()

        # Load canvas background
        self.canvas = cv2.imread("/app/gui.jpg")

        if self.queue_sector:
            # save the sector of the image to reset the number
            self.number_patch = self.canvas[
                565 - 100 : 565 + 100, 750 - 100 : 750 + 100
            ].copy()
            # use bold font for queue
            cv2.putText(
                self.canvas,
                f"{str(self.queue)}",
                (750, 565),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 255, 255),
                2,
            )
        else:
            # write "Not active" if queue sector is not defined
            cv2.putText(
                self.canvas,
                "Not active",
                (700, 545),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )

        cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Camera", WINDOW_WIDTH, WINDOW_HEIGHT)

        self.frame_num = 0

    def update_canvas(self):
        # Calculate dimensions
        cam_width = int(WINDOW_WIDTH * 0.49)
        cam_height = int(CAM_HEIGHT * cam_width / CAM_WIDTH)
        graph_width = cam_width
        graph_height = WINDOW_HEIGHT - cam_height
        text_pos_x = WINDOW_WIDTH - 220
        text_pos_y = WINDOW_HEIGHT - 120

        # Check if frame, heatmap, histogram are not None and are numpy arrays
        edge = 10
        if (
            self.histogram is not None
            and isinstance(self.histogram, np.ndarray)
            and self.histogram.size > 0
        ):
            self.canvas[
                -graph_height + edge + 5 : -edge,
                edge : graph_width + edge,
            ] = self.histogram[edge * 2 + 5 : graph_height, :graph_width]

        if (
            self.frame is not None
            and isinstance(self.frame, np.ndarray)
            and self.frame.size > 0
        ):
            self.canvas[edge : cam_height + edge, edge : cam_width + edge] = self.frame

        if (
            self.heatmap is not None
            and isinstance(self.heatmap, np.ndarray)
            and self.heatmap.size > 0
        ):
            self.canvas[
                edge : cam_height + edge, -cam_width - edge : -edge
            ] = self.heatmap

        if self.queue_sector and self.queue != self.prev_queue:
            print("Queue changed", self.prev_queue, self.queue)
            # delete previous queue, not elegant, but works
            self.canvas[
                565 - 100 : 565 + 100, 750 - 100 : 750 + 100
            ] = self.number_patch.copy()
            # use red if the number of people exceeds the limit
            if self.queue > self.queue_limit:
                color = (0, 0, 255)
            else:
                color = (255, 255, 255)
            cv2.putText(
                self.canvas,
                f"{str(self.queue)}",
                (750, 565),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                color,
                2,
            )

            self.prev_queue = self.queue

        cv2.imshow("Camera", self.canvas)

        return self.canvas

    def run(self):
        # Define video output parameters
        output_filename = "output_video.mp4"
        codec = cv2.VideoWriter_fourcc(*"mp4v")

        # Initialize the VideoWriter
        video_writer = cv2.VideoWriter(
            output_filename, codec, FPS, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        while True:
            start_time = time.time()
            print(f"Processing frame {self.frame_num}...")
            if self.updating:
                # Process the frame
                current_time = datetime.datetime.now()
                success = self.process_frame(current_time)
                if success is None:
                    end_time = time.time()
                    continue
                elif not success:
                    print("End of video file reached.")
                    break

                if self.frame is not None:
                    # Update the images
                    self.canvas = self.update_canvas()
                    # Write the canvas to the video file
                    video_writer.write(self.canvas)

            current_time = datetime.datetime.now()
            end_time = time.time()
            elapsed = end_time - start_time
            remaining = 1 / FPS - elapsed
            if remaining > 1:
                key = cv2.waitKey(int(remaining * 100)) & 0xFF
            else:
                key = cv2.waitKey(1) & 0xFF
            if key == ord("p") or key == ord(
                "P"
            ):  # Pause the application when 'p' is pressed
                self.updating = False
            elif key == ord("r") or key == ord(
                "R"
            ):  # Resume the application when 'r' is pressed
                self.updating = True
            elif key == 27:  # Exit the application when 'ESC' is pressed
                break

        # Release the VideoWriter and close the windows
        video_writer.release()
        cv2.destroyAllWindows()

    def process_frame(self, current_time):
        # Calculate dimensions
        cam_width = int(WINDOW_WIDTH * 0.49)
        cam_height = int(CAM_HEIGHT * cam_width / CAM_WIDTH)
        graph_width = cam_width
        graph_height = WINDOW_HEIGHT - cam_height

        # Increment frame number
        self.frame_num += 1

        # Read the next frame from the video
        frame = self.streamer.get_frame()
        if frame is None or frame is False:
            self.frame = None
            return frame

        # frame = cv2.resize(frame, (CAM_WIDTH, CAM_HEIGHT), interpolation=cv2.INTER_LINEAR)
        if self.person_detector.detections is not None:
            detections = self.person_detector.detections.copy()
            self.frame = self.person_detector.output_frame.copy()

        else:
            detections = None
            self.frame = None

        heatmap_thread = threading.Thread(
            target=self.heatmap_generator.create_heatmap,
            args=(detections, self.frame_num, 1),
        )
        histogram_thread = threading.Thread(
            target=self.histogram_generator.add_input, args=(detections, current_time)
        )
        detect_thread = threading.Thread(
            target=self.person_detector.detect, args=(frame.copy(), self.frame_num)
        )

        heatmap_thread.start()
        histogram_thread.start()
        detect_thread.start()
        heatmap_thread.join()
        histogram_thread.join()
        detect_thread.join()

        # Resize the image and update the canvas
        if self.frame is not None:
            if self.queue_sector:
                self.frame, self.queue = get_queue(
                    detections, self.queue_sector, self.frame
                )

            heatmap = cv2.resize(
                self.heatmap_generator.heatmap, (cam_width, cam_height)
            )
            self.heatmap = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame = cv2.resize(self.frame, (cam_width, cam_height))
            self.heatmap = cv2.resize(self.heatmap, (cam_width, cam_height))
            self.histogram = cv2.resize(
                self.histogram_generator.histogram_image, (graph_width, graph_height)
            )

            self.heatmap[:, :, 2] = (
                (self.heatmap[:, :, 2].astype(np.uint16) + heatmap.astype(np.uint16))
                .clip(0, 255)
                .astype(np.uint8)
            )

            # when the number of people exceeds self.queue_limit, send an email notification
            # only send the notification once every 2 minutes
            if (
                self.queue > self.queue_limit
                and (self.time_last_warning + datetime.timedelta(minutes=2))
                < datetime.datetime.now()
            ):
                email_address = "recipient@example.com"  # recipient email address
                subject = "People Count Exceeded"
                message = (
                    "The people count has exceeded the limit of 10. Current people count is "
                    + str(self.queue)
                )
                send_email(email_address, subject, message)
                print(" ------------- Email sent ------------- ")
                self.time_last_warning = datetime.datetime.now()

        return True


def send_email(email, subject, message):
    # Replace the placeholders with your Gmail account information
    YOUR_EMAIL = "meijiaojiaohappy@gmail.com"
    YOUR_PASSWORD = "bbbegyaiiilrqgaq"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = YOUR_EMAIL
    msg["To"] = email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(YOUR_EMAIL, YOUR_PASSWORD)
    try:
        server.send_message(msg)
    except:
        print("Error sending email")
    server.quit()


def get_queue(detections, rectangle, img):
    # Unpack rectangle coordinates
    x, y, x1, y1 = rectangle

    # Draw rectangle on the image
    cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 2)
    # write "Queue zone" on the left bottom corner of the rectangle
    cv2.rectangle(img, (x, y1 - 24), (x + 135, y1), (0, 255, 0), -1)
    cv2.putText(
        img,
        "Queue zone",
        (x, y1 - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )

    # Initialize counter
    counter = 0

    # Go through all detections and check if they are within the rectangle
    for detection in detections:
        frame, center_x, center_y = detection

        if x < center_x < x1 and y < center_y < y1:
            # Increment the counter if the center of detection is within the rectangle
            counter += 1

    return img, counter


def check_and_resize_video(input_path):
    # Capture the video from file
    cap = cv2.VideoCapture(input_path)

    # Check if video file is opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Get original video width and height
    orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # If the original dimensions are not 1280x720 then resize
    print(f"Original video dimensions: {orig_width}x{orig_height} pixels.")
    if orig_width != CAM_WIDTH or orig_height != CAM_HEIGHT:
        print("Resizing video... please wait, this may take a minute.")
        # Define the output path
        output_path = "resized_video.mp4"
        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # or use 'XVID'
        out = cv2.VideoWriter(
            output_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (CAM_WIDTH, CAM_HEIGHT)
        )

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Resize frame
                resized_frame = cv2.resize(frame, (CAM_WIDTH, CAM_HEIGHT))

                # write the resized frame
                out.write(resized_frame)
            else:
                break

        # Release everything when job is finished
        cap.release()
        out.release()

        print(f"Video was resized to {CAM_WIDTH}x{CAM_HEIGHT} pixels.")
        return output_path
    else:
        print("Video is already the correct size.")
        return input_path
