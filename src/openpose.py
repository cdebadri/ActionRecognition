import cv2 as cv
import numpy as np
import sys
import os

import pose_recognition as recog

class openpose:
    def __init__(self):
        proto_path = os.path.abspath(__file__ + '/../../models/pose_deploy_linevec.prototxt')
        model_path = os.path.abspath(__file__ + '/../../models/pose_iter_440000.caffemodel')
        self.net = cv.dnn.readNetFromCaffe(proto_path, model_path)

    def batch_process(self, frames):
        blob = cv.dnn.blobFromImages(frames, 1./255, (368, 368), (0, 0, 0), swapRB=False, crop=False)
        self.net.setInput(blob)
        out = self.net.forward()
        detected_points = np.zeros((frames.shape[0], 36))

        for i in range(frames.shape[0]):
            points = np.array([])
            for j in range(18):
                heatMap = out[i, j, :, :]
                heatMap = cv.resize(heatMap, (1280, 720))
                _, conf, _, point = cv.minMaxLoc(heatMap)
                if conf > 0.1:
                    points = np.append(points, [point[0], point[1]])
                else:
                    points = np.append(points, [0, 0])
            detected_points[i] = points

        return detected_points

    def process(self, frame):
        frame_height, frame_width = int(frame.shape[0]), int(frame.shape[1])
        blob = cv.dnn.blobFromImage(frame, 1./255, (64, 64), (0, 0, 0), swapRB=False, crop=False)
        self.net.setInput(blob)
        out = self.net.forward()
        points = np.array([])

        for j in range(18):
            heatMap = out[0, j, :, :]
            heatMap = cv.resize(heatMap, (frame_width, frame_height))
            _, conf, _, point = cv.minMaxLoc(heatMap)
            if conf > 0.1:
                points = np.append(points, [point[0], point[1]])
            else:
                points = np.append(points, [0, 0])

        return points

    @staticmethod
    def draw_points(frame, points):
        # draw the points for testing
        for i in range(0, len(points), 2):
            cv.circle(frame, (int(points[i]), int(points[i + 1])), 10, (255, 0, 0))
        return frame

openpose_obj = openpose()
recog_obj = recog.pose_recognition()

cap = cv.VideoCapture()
if len(sys.argv) == 1:
    cap.open(0)
else:
    cap.open(sys.argv[1])

# cap.set(3, 368)
frame_height, frame_width = cap.get(3), cap.get(4)
frame_rate = cap.get(5)
# cap.set(5, 1)

retval, points, index = True, np.zeros((32, 36), dtype=np.float32), 0
# frames = np.zeros((32, 720, 1280, 3), dtype=np.float32)
while True:
    retval, frame = cap.read()
    # print(openpose_obj.process(frame))

    if not retval:
        break

    # if image dimensions are smaller make them bigger
    # if frame_width < 1280 or frame_height < 720:
    #     frame = cv.resize(frame, (1280, 720))
    
    points[index] = openpose_obj.process(frame)
    # frames[index] = frame
    # frame = openpose.draw_points(frame, points[index])
    if index < 31:
        index += 1
    else:
        # points = openpose_obj.batch_process(frames)
        print(recog_obj.inference([points]))
        index = 0

    frame = cv.resize(frame, (640, 480))
    cv.imshow('frame', frame)
    if cv.waitKey(500) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()