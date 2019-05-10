import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter import messagebox
from openpose import openpose
from pose_recognition import pose_recognition

class App:
    def __init__(self, top,C, top_title, video_source, openpose_obj, recog_obj):
        self.top=top
        self.C=C
        self.top.title(top_title)
        self.video_source=video_source
        self.count=0
    
        self.vid = MyVideoCapture(self.video_source)
        self.openpose_obj = openpose_obj
        self.recog_obj = recog_obj
        self.points = np.zeros((32, 36), dtype=np.float32)
        self.index = 0
        self.pose_output = StringVar()
        self.pose_output.set('pose output to be displayed here')

        self.B=Button(pw2, text="Stop Video",command=self.count_set)
        pw2.add(self.B)

        self.r = Label(pw, textvariable=self.pose_output, padx=100)
        pw.add(self.r)
        
        self.delay = 15
        self.update()

        # self.top.mainloop()

    def count_set(self):
        self.count=1
        self.B.destroy()
        self.r.destroy()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        global pose_output
        if ret:
            if self.index < 31:
                self.points[self.index] = self.openpose_obj.process(frame)
                frame = openpose.draw_points(frame, self.points[self.index])
                self.index += 1
            else:
                pose = self.recog_obj.inference([self.points])
                self.pose_output.set(pose)
                self.index = 0
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.C.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        if(self.count==0):
            self.top.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source):
        self.video_source=video_source
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
 
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                if frame.shape[1] < 1280 or frame.shape[0] < 720:
                    frame = cv2.resize(frame, (1280, 720))
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

def livevideo(openpose_obj, recog_obj):
    App(top,C, "Action Recognizer",0, openpose_obj, recog_obj)

def myvideo(openpose_obj, recog_obj):
    filename=askopenfilename()
    App(top,C, "Action Recognizer",filename, openpose_obj, recog_obj)

if __name__ == '__main__':
    openpose_obj = openpose()
    recog_obj = pose_recognition()

    top=tkinter.Tk()

    pw=PanedWindow()
    pw.pack(fill=BOTH,expand=1)

    pw1=PanedWindow(pw,orient=VERTICAL)
    pw.add(pw1)
    #Creating the canvas
    C=Canvas(pw1, bg = "blue", height = 480, width = 640)
    pw1.add(C)

    pw2=PanedWindow(pw1)
    pw1.add(pw2)    
    #Creating the menu button
    mb= Menubutton(pw2, text = "Get Video Clip", relief = RAISED,padx=125)
    mb.menu = Menu(mb,tearoff=0)
    mb["menu"]  =  mb.menu
    mb.menu.add_command(label="Take video", command=lambda: livevideo(openpose_obj, recog_obj))
    mb.menu.add_command(label="Open a video file", command=lambda: myvideo(openpose_obj, recog_obj))
    pw2.add(mb)

    # r=Label(pw, text=pose_output,padx=100)
    # print(pose_output)
    # r = Label(pw, textvariable=pose_output, padx=100)
    # pw.add(r)

    top.mainloop()
