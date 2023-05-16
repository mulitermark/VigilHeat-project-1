import numpy as np
import cv2
from person_detector import PersonDetector
from heatmap_generator import HeatmapGenerator

def main():
    # Set video input path
    video_path = 'test.mp4'

    # person_detector = PersonDetector(video_path)
    # person_detector.detect()
    # person_detector.save_detections("detections.npy")

    heatmap_generator = HeatmapGenerator("detections.npy", 1270, 720)
    heatmap_generator.create_heatmap(0, 3000, 1)

    return 0

if __name__ == "__main__":
    main()