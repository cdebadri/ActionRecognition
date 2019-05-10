import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
from tkinter.filedialog import askopenfilename
from tkinter import *
from openpose import openpose
from pose_recognition import pose_recognition
import os

class App:
    def __init__(self, root, openpose_obj, recog_obj):
        self.root = root
        self.openpose_obj = openpose_obj
        self.recog_obj = recog_obj
        self.source = Capture()
        self.delay = 15
        self.points = np.zeros((32, 36), dtype=np.float32)
        self.index = 0
        self.pose_numeric = -1

        self.window = PanedWindow()
        self.window.pack(fill=BOTH, expand=1)

        self.pane = PanedWindow(self.window, orient=VERTICAL)
        self.window.add(self.pane)

        self.canvas = Canvas(self.pane, bg = "blue", height = 480, width = 640)
        self.pane.add(self.canvas)

        self.pane2 = PanedWindow(self.pane)
        self.pane.add(self.pane2)

        self.get_video = Menubutton(self.pane2, text='Get Video Clip', relief=RAISED, padx=125)
        self.get_video.menu = Menu(self.get_video, tearoff=0)
        self.get_video['menu'] = self.get_video.menu
        self.get_video.menu.add_command(label="Take video", command=lambda: self.livevideo())
        self.get_video.menu.add_command(label="Open a video file", command=lambda: self.myvideo())
        self.pane2.add(self.get_video)

        self.stop_button = Button(self.pane2, text='Stop Video', state='disabled', command=self.count_set)
        self.pane2.add(self.stop_button)

        self.class_label = PIL.Image.open(os.path.abspath(__file__ + '/../../assets/default.jpg'))
        self.class_label.thumbnail((240, 240), PIL.Image.ANTIALIAS)
        self.default_label = self.class_label
        self.output_image = PIL.ImageTk.PhotoImage(self.class_label)
        self.pose_output = StringVar()
        self.pose_output.set('Pose Label to be displayed here')
        self.output = Label(self.window, image=self.output_image , textvariable=self.pose_output,
                            compound=TOP, font=('Helvitica', 16), padx=10, pady=50)
        self.window.add(self.output)

        self.count = 0
        
        # self.source = Capture()
        # self.delay = 15
        self.update()

    def livevideo(self):
        self.source.open_webcam()
        self.get_video.config(state='disabled')
        self.stop_button.config(state='normal')
        self.pose_numeric = 6
        self.action()
        return

    def myvideo(self):
        self.source.open_file()
        self.get_video.config(state='disabled')
        self.stop_button.config(state='normal')
        self.pose_numeric = 6
        self.action()
        return

    def count_set(self):
        self.source.release_source()
        self.canvas.delete(self.image_tag)
        self.stop_button.config(state='disabled')
        self.get_video.config(state='normal')
        self.pose_numeric = -1
        self.action()

    def update(self):
        ret, frame = self.source.get_frames()
        if ret:
            if self.index < 31:
                self.points[self.index] = self.openpose_obj.process(frame)
                frame = openpose.draw_points(frame, self.points[self.index])
                self.index += 1
            else:
                self.pose_numeric = self.recog_obj.inference([self.points])
                self.action()
                self.index = 0
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.image_tag = self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        if(self.count == 0):
            self.root.after(self.delay, self.update)
        return

    def action(self):
        if self.pose_numeric == 0:
            self.class_label = PIL.Image.open(os.path.abspath(__file__ + '/../../assets/jumping.png'))
            self.pose_output.set('Jumping')
        elif self.pose_numeric == 1:
            self.class_label = PIL.Image.open(os.path.abspath(__file__ + '/../../assets/jumping_jacks.png'))
            self.pose_output.set('Jumping Jacks')
        elif self.pose_numeric == 2:
            self.class_label = PIL.Image.open(os.path.abspath(__file__ + '/../../assets/boxing.gif'))
            self.pose_output.set('Boxing')
        elif self.pose_numeric == 3:
            self.class_label = PIL.Image.open(os.path.abspath(__file__ + '/../../assets/waving_2_hands.jpg'))
            self.pose_output.set('Waving Both Hands')
        elif self.pose_numeric == 4:
            self.class_label = PIL.Image.open(os.path.abspath(__file__ + '/../../assets/waving_1_hand.jpg'))
            self.pose_output.set('Waving One Hand')
        elif self.pose_numeric == 5:
            self.class_label = PIL.Image.open(os.path.abspath(__file__ + '/../../assets/clapping.png'))
            self.pose_output.set('Clapping')
        elif self.pose_numeric == -1:
            self.class_label = PIL.Image.open(os.path.abspath(__file__ + '/../../assets/default.jpg'))
            self.pose_output.set('Pose Label to be displayed here')
        elif self.pose_numeric == 6:
            self.class_label = PIL.Image.open(os.path.abspath(__file__ + '/../../assets/thinking.png'))
            self.pose_output.set('Thinking...')
        
        self.class_label.thumbnail((240, 240), PIL.Image.ANTIALIAS)
        self.output_image = PIL.ImageTk.PhotoImage(self.class_label)
        self.output.configure(image=self.output_image)
        return


class Capture:
    def __init__(self):
        self.source = cv2.VideoCapture()

    def open_webcam(self):
        if not self.source.isOpened():
            self.source.open(0)
        if not self.source.isOpened():
            raise ValueError("Unable to open video source", 0)
        return

    def open_file(self):
        if not self.source.isOpened():
            filename = askopenfilename()
            self.source.open(filename)
        if not self.source.isOpened():
            raise ValueError("Unable to open video source", filename)    
        return

    def get_frames(self):
        if self.source.isOpened():
            ret, frame = self.source.read()
            if ret:
                if frame.shape[1] < 1280 or frame.shape[0] < 720:
                    frame = cv2.resize(frame, (1280, 720))
                return (ret, frame)
            else:
                return (ret, None)
        return (False, None)

    def release_source(self):
        if self.source.isOpened():
            self.source.release()


if __name__ == '__main__':
    openpose_obj = openpose()
    recog_obj = pose_recognition()

    root = tk.Tk()
    root.title('Action Recognizer')
    root.resizable(0, 0)
    App(root, openpose_obj, recog_obj)
    root.mainloop()

