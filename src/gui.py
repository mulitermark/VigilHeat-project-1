import datetime
import cv2
import numpy as np

from person_detector import PersonDetector
from heatmap_generator import HeatmapGenerator
from stream_handler import VideoStreamHandler
from histogram_generator import HistogramGenerator

class Application:
    def __init__(self, height=600, width=800, channels=3):
        self.updating = True
        self.frame = None
        self.heatmap = None
        self.histogram = None

        self.heatmap_generator = HeatmapGenerator(1270, 720)
        self.histogram_generator = HistogramGenerator("minute")

        video_path = 'test.mp4'
        self.streamer = VideoStreamHandler(video_path)
        self.person_detector = PersonDetector()

        # Create an empty canvas
        self.canvas = np.zeros((height, width, channels), dtype=np.uint8)

        cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Camera', width, height)

        self.frame_num = 0

    def update_canvas(self, canvas, frame, heatmap, histogram, height=600, width=800):
        # Calculate dimensions
        cam_width = max(int(width * 0.6), 1)
        cam_height = height
        graph_width = max(int(width * 0.4), 1)
        graph_height = max(int(height / 2), 1)

        # Check if frame, heatmap, histogram are not None and are numpy arrays
        if frame is not None and isinstance(frame, np.ndarray) and frame.size > 0:
            # Resize the image and update the canvas
            frame_resized = cv2.resize(frame, (cam_width, cam_height))
            canvas[:cam_height, :cam_width] = frame_resized

        if heatmap is not None and isinstance(heatmap, np.ndarray) and heatmap.size > 0:
            # Resize the image and update the canvas
            heatmap_resized = cv2.resize(heatmap, (graph_width, graph_height))
            canvas[:graph_height, cam_width:, 2] = heatmap_resized

        if histogram is not None and isinstance(histogram, np.ndarray) and histogram.size > 0:
            # Resize the image and update the canvas
            histogram_resized = cv2.resize(histogram, (graph_width, graph_height))
            canvas[graph_height:, cam_width:] = histogram_resized

        cv2.imshow('Camera', canvas)

        return canvas

    def run(self, height=600, width=800):
        # Define video output parameters
        output_filename = 'output_video.mp4'
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        fps = 30

        # Initialize the VideoWriter
        video_writer = cv2.VideoWriter(output_filename, codec, fps, (width, height))

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('p'):  # Pause the application when 'p' is pressed
                self.updating = False
            elif key == ord('r'):  # Resume the application when 'r' is pressed
                self.updating = True
            elif key == 27:  # Exit the application when 'ESC' is pressed
                break

            print(f"Processing frame {self.frame_num}...")
            current_time = datetime.datetime.now()
            if self.updating:
                # Process the frame
                self.process_frame(current_time)
                if self.frame is None:
                    return

                # Update the images
                self.canvas = self.update_canvas(self.canvas, self.frame, self.heatmap, self.histogram)

                # Write the canvas to the video file
                video_writer.write(self.canvas)

        # Release the VideoWriter and close the windows
        video_writer.release()
        cv2.destroyAllWindows()

    def process_frame(self,current_time ):
        # Increment frame number
        self.frame_num += 1

        # Read the next frame from the video
        self.frame = self.streamer.get_frame()
        if self.frame is None:
            return

        self.frame, detections = self.person_detector.detect(self.frame, self.frame_num)
        self.heatmap = self.heatmap_generator.create_heatmap(detections, self.frame_num, 1)

        self.histogram = self.histogram_generator.add_input(detections, current_time)
