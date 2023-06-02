import numpy as np
import cv2
from scipy.ndimage.filters import gaussian_filter


class HeatmapGenerator:
    def __init__(self, video_width, video_height):
        self.video_width = video_width
        self.video_height = video_height
        self.detection_map = np.zeros((video_height, video_width), dtype=np.uint32)
        self.heatmap = np.zeros((video_height, video_width), dtype=np.uint8)

    def create_heatmap(self, detections, frame_num, heatmap_intensity_scale_factor):
        if detections is None or len(detections) == 0:
            self.heatmap = self.heatmap
            return

        self.detection_map[detections[:, 2], detections[:, 1]] += 1

        multiplier = 2550000 / frame_num * heatmap_intensity_scale_factor
        self.heatmap = (gaussian_filter(self.detection_map.astype(float), sigma=20) * multiplier).clip(0, 255).astype(np.uint8)
