from queue import Queue
from pose_recognition import pose_recognition
from openpose import openpose
import time
import os
import cv2
import numpy as np

class project_x(pose_recognition, openpose):
    def __init__(self):
        super(openpose, self).__init__()
        super(pose_recognition, self).__init__()
        self.frame_queue = Queue()
        self.points_queue = Queue(maxsize=32)
        self.END_FRAME = False

    def readVideo(source, kill=None):
        cap = cv2.VideoCapture(source)
        while not self.END_FRAME:
            retval, frame = cap.read()
            if not retval:
                self.END_FRAME = True
                break
            self.frame_queue.put(frame)
            frame = cv2.resize(frame, (640, 480))
            cv2.imshow('camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.END_FRAME = True
                cap.release()
                cap.destroyAllWindows()

            print('frame')
        
        # cap.release()
        # cap.destroyAllWindows()

    def getPoints():
        points = np.zeros((36), dtype=np.float32)
        while not self.END_FRAME and (cv2.waitKey(1) & 0xFF == ord('q')):
            if self.frame_queue.empty():
                time.sleep(10)
            if not self.points_queue.full():
                points = super(openpose, self).process(self.frame_queue.get())
                self.points_queue.put(points)

            print('points')
        
    def recognizeAct():
        print('recog')
        data = np.zeros((32, 36), dtype=np.float32)
        while not self.END_FRAME and (cv2.waitKey(1) & 0xFF == ord('q')):
            if self.points_queue.full():
                for i in range(32):
                    data[i] = self.points_queue.get()
                print(super(pose_recognition, self).inference([data]))
            else:
                time.sleep(1000)

            