import cv2


class VideoStreamHandler:
    def __init__(self, video_path):
        self.video_path = video_path
        self.video = cv2.VideoCapture(video_path)
        self.counter = 0
    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        self.counter += 1 
        if ret and self.counter % 3 == 0:
            # Convert the frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame
        else:
            return None
