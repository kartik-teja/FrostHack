import cv2
import imutils
import numpy as np
from collections import deque

class VideoProcessor:
    def __init__(self, model_path="./HAR/resnet-34_kinetics.onnx", classes_path="./HAR/Actions.txt", input_path=0):
        self.CLASSES = open(classes_path).read().strip().split("\n")
        self.SAMPLE_DURATION = 16
        self.SAMPLE_SIZE = 112
        self.frames = deque(maxlen=self.SAMPLE_DURATION)
        self.net = cv2.dnn.readNet(model_path)
        self.vs = cv2.VideoCapture(input_path)

    def process_video(self):
        class_counts = {label: 0 for label in self.CLASSES}

        while True:
            (grabbed, frame) = self.vs.read()

            if not grabbed:
                print("[INFO] No frame read from the video stream - Exiting...")
                break

            frame = imutils.resize(frame, width=400)
            self.frames.append(frame)

            if len(self.frames) < self.SAMPLE_DURATION:
                continue

            blob = cv2.dnn.blobFromImages(self.frames, 1.0, (self.SAMPLE_SIZE, self.SAMPLE_SIZE),
                                          (114.7748, 107.7354, 99.4750), swapRB=True, crop=True)
            blob = np.transpose(blob, (1, 0, 2, 3))
            blob = np.expand_dims(blob, axis=0)

            self.net.setInput(blob)
            outputs = self.net.forward()
            label = self.CLASSES[np.argmax(outputs)]

            cv2.rectangle(frame, (0, 0), (300, 40), (0, 0, 0), -1)
            cv2.putText(frame, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            cv2.imshow("Activity Recognition", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        self.vs.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    video_processor = VideoProcessor()
    video_processor.process_video()
