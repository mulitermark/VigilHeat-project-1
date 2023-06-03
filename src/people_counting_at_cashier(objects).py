import datetime

import cv2
import argparse

import pandas as pd
from matplotlib import pyplot as plt
from ultralytics import YOLO
import supervision as sv
import numpy as np

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument("--input", type=str, default="webcam", help="Input video file path or 'webcam' (default)")
    parser.add_argument("--webcam-resolution", default=[1280, 720], nargs=2, type=int, help="Webcam video resolution")
    parser.add_argument("--output", type=str, help="Output video file path")
    parser.add_argument("--skip-frames", type=int, default=1, help="Number of frames to skip (default is 10)")
    parser.add_argument("--email", type=str, help="Email address for sending notification")
    args = parser.parse_args()
    return args


def draw_heatmap(frame, detections):
    heatmap = np.zeros(frame.shape[:2], dtype=np.float32)

    for detection in detections:
        bbox, _, _, _ = detection

        if bbox is None:
            continue

        xmin, ymin, xmax, ymax = bbox
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)

        # create a heatmap on which we will add all the bounding boxes
        heatmap[ymin:ymax, xmin:xmax] += 1

    heatmap = cv2.normalize(heatmap, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # 将热力图应用于原始帧图像
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap = cv2.addWeighted(frame, 0.7, heatmap, 0.3, 0)

    return heatmap


def send_email(email, subject, message):
    # Replace the placeholders with your Gmail account information
    YOUR_EMAIL = "meijiaojiaohappy@gmail.com"
    YOUR_PASSWORD = "bbbegyaiiilrqgaq"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = YOUR_EMAIL
    msg['To'] = email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(YOUR_EMAIL, YOUR_PASSWORD)
    server.send_message(msg)
    server.quit()


def main():
    # create an empty DataFrame
    df = pd.DataFrame(columns=["Time", "People Count"])

    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    if args.input == "webcam":
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    else:
        cap = cv2.VideoCapture(args.input)

    out = None

    if args.output:
        output_width, output_height = frame_width, frame_height
        out = cv2.VideoWriter(
            args.output,
            cv2.VideoWriter_fourcc(*"mp4v"),
            25,
            (output_width, output_height)
        )

    # load yolov8l.pt model
    model = YOLO("yolov8l.pt")

    # set box_annotator
    box_annotator = sv.BoxAnnotator(
        thickness=1,
        text_thickness=1,
        text_scale=0.5
    )

    skip_frames = args.skip_frames
    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        if frame_count % skip_frames != 0:
            continue

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)

        labels = [f"{model.model.names[class_id]} {confidence:0.2f}"
                  for _, confidence, class_id, _
                  in detections]

        frame = box_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels
        )

        for index, detection in enumerate(detections):
            if model.model.names[detection[2]] != 'person':
                detections.confidence[index] = 0

        detections = detections[detections.confidence > 0]

        # show total number of people on the screen
        cv2.putText(frame, "Total number of people: " + str(len(detections)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)
        # show date and time on the screen, datatime imported from datetime, day hour minute second
        cv2.putText(frame, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # count the number of people
        people_count = len(detections)
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # add the current time and people count to the DataFrame
        df = pd.concat([df, pd.DataFrame([[current_time, people_count]], columns=["Time", "People Count"])])

        if len(detections) > 10 and args.email:
            email_address = args.email
            subject = "People Count Exceeded"
            message = "The people count has exceeded the limit of 10. Current people count is " + str(len(detections))
            send_email(email_address, subject, message)
        elif len(detections) < 5 and args.email:
            email_address = args.email
            subject = "Low People Count"
            message = "The people count is below 5. Consider reducing the workforce. Current people count is " + str(
                len(detections))
            send_email(email_address, subject, message)

        if len(detections) == 0:
            # if no people detected, continue
            continue

        heatmap = draw_heatmap(frame, detections)

        if args.output and out is not None:
            out.write(heatmap)

        cv2.imshow("People Counting", heatmap)

        if cv2.waitKey(30) == 27:
            break

    # print statistics like max and min people count
    print("Max people count: ", df["People Count"].max())
    print("Min people count: ", df["People Count"].min())
    # plot the people count by time and save it as a png file
    df.plot(x="Time", y="People Count", kind="line")
    plt.savefig("people_count.png")

    # save the people count as a csv file
    df.to_csv("people_count.csv", index=False)

    if args.output and out is not None:
        out.release()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
