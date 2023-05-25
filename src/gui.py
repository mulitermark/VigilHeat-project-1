import datetime
import cv2
import numpy as np
import time

from person_detector import PersonDetector
from heatmap_generator import HeatmapGenerator
from stream_handler import VideoStreamHandler
from histogram_generator import HistogramGenerator

FPS = 30
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
CAM_WIDTH = 1280
CAM_HEIGHT = 720

class Application:
    def __init__(self):
        self.updating = True
        self.frame = None
        self.heatmap = None
        self.histogram = None

        self.heatmap_generator = HeatmapGenerator(CAM_WIDTH, CAM_HEIGHT)
        self.histogram_generator = HistogramGenerator("minute")

        video_path = 'test.mp4'
        self.streamer = VideoStreamHandler(video_path)
        self.person_detector = PersonDetector()

        # Create an empty canvas
        self.canvas = np.ones((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8) * 255
        text_pos_x = WINDOW_WIDTH - 220
        text_pos_y = WINDOW_HEIGHT - 120
        cv2.putText(self.canvas, "CONTROLS:", (text_pos_x, text_pos_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(self.canvas, "Esc: Exit application", (text_pos_x, text_pos_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        cv2.putText(self.canvas, "P: Pause application", (text_pos_x, text_pos_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        cv2.putText(self.canvas, "R: Resume application", (text_pos_x, text_pos_y + 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Camera', WINDOW_WIDTH, WINDOW_HEIGHT)

        self.frame_num = 0

    def update_canvas(self, canvas, frame, heatmap, histogram):
        # Calculate dimensions
        cam_width = int(WINDOW_WIDTH * 0.49)
        cam_height = int(CAM_HEIGHT * cam_width / CAM_WIDTH)
        graph_width = cam_width
        graph_height = WINDOW_HEIGHT - cam_height

        # Check if frame, heatmap, histogram are not None and are numpy arrays
        if frame is not None and isinstance(frame, np.ndarray) and frame.size > 0:
            # Resize the image and update the canvas
            frame_resized = cv2.resize(frame, (cam_width, cam_height))
            canvas[:cam_height, :cam_width] = frame_resized

        if heatmap is not None and isinstance(heatmap, np.ndarray) and heatmap.size > 0:
            # Resize the image and update the canvas
            heatmap_resized = cv2.resize(heatmap, (cam_width, cam_height))
            canvas[:cam_height, -cam_width:] = heatmap_resized

        if histogram is not None and isinstance(histogram, np.ndarray) and histogram.size > 0:
            # Resize the image and update the canvas
            histogram_resized = cv2.resize(histogram, (graph_width, graph_height))
            canvas[-graph_height:, :graph_width] = histogram_resized

        cv2.imshow('Camera', canvas)

        return canvas

    def run(self):
        # Define video output parameters
        output_filename = 'output_video.mp4'
        codec = cv2.VideoWriter_fourcc(*'mp4v')

        # Initialize the VideoWriter
        video_writer = cv2.VideoWriter(output_filename, codec, FPS, (WINDOW_WIDTH, WINDOW_HEIGHT))

        while True:
            start_time = time.time()
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

            current_time = datetime.datetime.now()
            end_time = time.time()
            elapsed = end_time - start_time
            remaining = 1 / FPS - elapsed
            if remaining > 0:
                key = cv2.waitKey(int(remaining * 100)) & 0xFF
            else:
                key = cv2.waitKey(1) & 0xFF
            if key == ord('p') or key == ord('P'):  # Pause the application when 'p' is pressed
                self.updating = False
            elif key == ord('r') or key == ord('R'):  # Resume the application when 'r' is pressed
                self.updating = True
            elif key == 27:  # Exit the application when 'ESC' is pressed
                break

        # Release the VideoWriter and close the windows
        video_writer.release()
        cv2.destroyAllWindows()

    def process_frame(self, current_time):
        # Increment frame number
        self.frame_num += 1

        # Read the next frame from the video
        frame = self.streamer.get_frame()
        if frame is None:
            self.frame = None
            return

        self.frame, detections = self.person_detector.detect(frame.copy(), self.frame_num)
        heatmap = self.heatmap_generator.create_heatmap(detections, self.frame_num, 1)
        self.heatmap = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.heatmap[:, :, 2] = (self.heatmap[:, :, 2].astype(np.uint16) + heatmap.astype(np.uint16)).clip(0, 255).astype(np.uint8)

        self.histogram = self.histogram_generator.add_input(detections, current_time)
