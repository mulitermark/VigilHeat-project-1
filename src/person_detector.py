from stream_handler import VideoStreamHandler
import torch
import numpy as np
import cv2

class PersonDetector:
    def __init__(self, video_path):
        # Open the video file
        self.streamer = VideoStreamHandler(video_path)

        # Load YOLOv5 model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        self.model.conf = 0.25
        self.model.classes = [0]
        self.detections = []

    def detect(self):
        frame_num = 0
        while True:
            frame_num += 1
            # Read the next frame from the video
            frame = self.streamer.get_frame()
            if frame is None:
                break

            # Perform person detection on the frame
            results = self.model(frame)

            # Draw bounding boxes and labels on the frame
            results.render()

            # get bounding boxes of people and calculate the position where they are standing
            bboxes = results.xyxy[0].cpu().numpy()
            ground_positions = np.zeros((bboxes.shape[0], 2), dtype=int)
            ground_positions[:, 0] = ((bboxes[:, 0] + bboxes[:, 2]) / 2).clip(0, frame.shape[1] - 1)
            ground_positions[:, 1] = bboxes[:, 3].clip(0, frame.shape[0] - 1)

            # add this frame to detections
            for center in ground_positions:
                self.detections.append(np.array([frame_num, center[0], center[1]], dtype=np.uint32))

            # Convert the frame back to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # draw circles to the positions where people are standing
            for center in ground_positions:
                cv2.circle(frame, center, 10, 0, -1)

            # Display the resulting frame
            cv2.imshow('YOLOv5 Person Detection', frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) == ord('q'):
                break

    def save_detections(self, path):
        np.save(path, np.array(self.detections))
