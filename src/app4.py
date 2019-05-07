import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter import messagebox
from openpose import openpose
from pose_recogntion import pose_recogntion

class App:
    def __init__(self, top,C, top_title, video_source):
        self.top=top
        self.C=C
        self.top.title(top_title)
        self.video_source=video_source
        self.count=0
    
        self.vid = MyVideoCapture(self.video_source)

        self.B=Button(pw2, text="Stop Video",command=self.count_set)
        pw2.add(self.B)
        
        self.delay = 15
        self.update()

        # self.top.mainloop()

    def count_set(self):
        self.count=1
        self.B.destroy()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
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
                # Return a boolean success flag and the current frame
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


def livevideo():
    App(top,C, "Tkinter and OpenCV",0)

def myvideo():
    filename=askopenfilename()
    App(top,C, "Tkinter and OpenCV",filename)

if __name__ == '__main__':
    # openpose_obj = openpose()
    # recog_obj = pose_recognition()

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
    mb.menu.add_command(label="Take video", command=livevideo)
    mb.menu.add_command(label="Open a video file", command=myvideo)
    pw2.add(mb)

    r=Label(pw, text="pose_output",padx=100)
    pw.add(r)

    top.mainloop()
