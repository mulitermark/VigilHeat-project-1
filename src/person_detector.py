from stream_handler import VideoStreamHandler
import torch
import numpy as np
import cv2



import cv2
from openvino.inference_engine import IECore

class PersonDetectorOpenVino:
    def __init__(self, model_path_xml, model_path_bin):
        # Load the OpenVINO model
        self.ie = IECore()
        self.net = self.ie.read_network(model_path_xml, model_path_bin)
        self.exec_net = self.ie.load_network(self.net, 'CPU')
        self.input_name = next(iter(self.net.input_info))

    def detect(self, frame, frame_num):
        # Prepare the frame for inference
        input_frame = cv2.resize(frame, (self.net.input_info[self.input_name].tensor_desc.dims[3], self.net.input_info[self.input_name].tensor_desc.dims[2]))
        input_frame = input_frame.transpose((2, 0, 1))
        input_frame = input_frame.reshape(1, *input_frame.shape)

        # Perform person detection on the frame
        outputs = self.exec_net.infer({self.input_name: input_frame})

        # Get the output layer containing the bounding box information
        output_name = next(iter(self.net.outputs))
        output_data = outputs[output_name]

        # Extract bounding boxes and calculate the positions where people are standing
        bboxes = output_data[0, 0]
        ground_positions = []
        # bboxes = bboxes[bboxes[:,2] > 0.94]
        for bbox in bboxes:
            if bbox[2] >= 0.94:  # Confidence threshold
                x_min = int(bbox[3] * frame.shape[1])
                y_min = int(bbox[4] * frame.shape[0])
                x_max = int(bbox[5] * frame.shape[1])
                y_max = int(bbox[6] * frame.shape[0])
                
                # Ensure bounding box coordinates are within valid range
                x_min = max(0, min(x_min, frame.shape[1] - 1))
                y_min = max(0, min(y_min, frame.shape[0] - 1))
                x_max = max(0, min(x_max, frame.shape[1] - 1))
                y_max = max(0, min(y_max, frame.shape[0] - 1))

                center_x = (x_min + x_max) // 2
                center_y = y_max
                ground_positions.append([center_x, center_y])

        single_image_detections = []
        # Add this frame's detections
        for center in ground_positions:
            single_image_detections.append(np.array([frame_num, center[0], center[1]], dtype=np.uint32))

        # Draw circles at the positions where people are standing
        for center in ground_positions:
            cv2.circle(frame, tuple(center), 10, (0, 0, 255), -1)

        return frame, np.array(single_image_detections)

    def save_detections(self, path):
        np.save(path, np.array(self.detections))


class PersonDetector:
    def __init__(self):

        # Load YOLOv5 model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        self.model.conf = 0.25
        self.model.classes = [0]

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

        return frame, np.array(single_image_detectons)

    def save_detections(self, path):
        np.save(path, np.array(self.detections))
