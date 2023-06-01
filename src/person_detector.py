from stream_handler import VideoStreamHandler
import torch
import numpy as np
import cv2

class PersonDetector:
    def __init__(self):

        # Load YOLOv5 model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        self.model.conf = 0.25
        self.model.classes = [0]
        self.output_frame = None
        self.detections = None

    def detect(self, frame, frame_num):

        # Perform person detection on the frame
        results = self.model(frame)

        # Draw bounding boxes and labels on the frame
        results.render()

        # get bounding boxes of people and calculate the position where they are standing
        bboxes = results.xyxy[0].cpu().numpy()
        ground_positions = np.zeros((bboxes.shape[0], 2), dtype=int)
        ground_positions[:, 0] = ((bboxes[:, 0] + bboxes[:, 2]) / 2).clip(0, frame.shape[1] - 1)
        ground_positions[:, 1] = bboxes[:, 3].clip(0, frame.shape[0] - 1)

        single_image_detectons = []
        # add this frame to detections
        for center in ground_positions:
            single_image_detectons.append(np.array([frame_num, center[0], center[1]], dtype=np.uint32))

        # Convert the frame back to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # draw circles to the positions where people are standing
        for center in ground_positions:
            cv2.circle(frame, center, 10, 0, -1)

        self.output_frame = frame
        self.detections = np.array(single_image_detectons)

    def save_detections(self, path):
        np.save(path, np.array(self.detections))
