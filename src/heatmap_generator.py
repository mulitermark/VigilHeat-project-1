import numpy as np
import cv2
from scipy.ndimage.filters import gaussian_filter

class HeatmapGenerator:
    def __init__(self, video_width, video_height):
        self.video_width = video_width
        self.video_height = video_height
        self.detection_map = np.zeros((video_height, video_width), dtype=np.uint32)
        self.heatmap = np.zeros((video_height, video_width), dtype=np.uint8)

    def create_heatmap(self, detections, first_frame, last_frame, heatmap_intesity_scale_factor):
        for detection in detections:
            self.detection_map[detection[2], detection[1]] += 1

        self.heatmap = (gaussian_filter(self.detection_map.astype(float), sigma=20) * 2550000 / heatmap_intesity_scale_factor).clip(0, 255).astype(np.uint8)
        return self.heatmap
