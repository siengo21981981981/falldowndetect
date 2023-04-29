
import window
import threading
import cv2
import calculate
import control_center
import tkinter as tk
import customtkinter as ck
import tensorflow as tf
from PIL import ImageTk
import mediapipe as mp_pose
import mediapipe as mp
import time
import pandas as pd
import numpy as np
from collections import deque

from sklearn.preprocessing import MinMaxScaler
import math as m
import PIL.Image, PIL.ImageTk

class body_detect():
    imgtk = None
    textbox = None
    m =None
    def __init__(self,video_path):#video_source,classname
        
        all_objects = []
        count = 0
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        
        self.pose = self.mp_pose.Pose()
         
        
        self.vid = cv2.VideoCapture(video_path)
        self.findBody()
    def findBody(self):
            global imgtk,textbox,m
            while True:
            # read a frame from the video stream
            
                ret, frame = self.vid.read()
                 
            
                if frame is None:
                    break
                if ret:
               
                  with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
                    h, w = frame.shape[:2]  # 960, 540
                    
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                       # image.flags.writeable = False
                    results = self.pose.process(image)
                   # image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    
                    msec = self.vid.get(cv2.CAP_PROP_POS_MSEC)
                    frame_count = self.vid.get(cv2.CAP_PROP_POS_FRAMES)
                    
                    self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                      self.mp_drawing.DrawingSpec(
                                          color=(245, 117, 66), thickness=2, circle_radius=4),
                                      self.mp_drawing.DrawingSpec(
                                          color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )
                    
                    second = 0
                    Angle0 = 0
                    
                    frame_check = False 
                    lm = results.pose_landmarks
                    lmPose = self.mp_pose.PoseLandmark
                    #(calculate(results,mp_pose,lm,lmPose,h,w,frame_count,msec))
                   
                    try:
                        #memory_test = [results ,frame ,self.vid ,self.label_value.falldown, self.label_value_fine, img, imgtk, self.canvas.image]
                        label_value_falldown ,label_value_fine = (calculate.Falldetect.calculate(results,self.mp_pose,lm,lmPose,h,w,frame_count,msec))
                        
                        
                        
                        m=min(label_value_fine[0],label_value_falldown[0])
                        if m is not None:
                            window.VideoApp.compare(self = window.textbox,m=m,label_value_falldown =label_value_falldown,label_value_fine = label_value_fine)
                        #print(m,",",label_value_fine[0],",",label_value_falldown[0])
                        
                        

                    except:
                        pass
                    
                    img = PIL.Image.fromarray(image)
                    imgtk = ImageTk.PhotoImage(img)
                    
                    
                    
                    if imgtk is not None:
                        window.VideoApp.cavas(self=window.canvas,imgtk=0)
                    time.sleep(0.001)
                        #photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(bgr_frame))
               # display the frame on the canvas
                    
                        
                         
                    '''self.canvas.itemconfig(self.canvas.create_image(0, 0, image=imgtk, anchor=tk.NW))
                    self.canvas.image = imgtk'''  # store reference to photo to prevent garbage collection
                        #print("self.canvas.image f{}",type(self.canvas.image))  
                    
                    '''try:    
                        del image, self.canvas.image 
                        
                    except:
                        pass'''
        # wait for a short time
  
                       
                         
classname ="0"
video = "D:/user/Desktop/TrainingVideo_falldown/3_New.avi"
if __name__ == '__main__':
    body_detect('D:/user/Desktop/TrainingVideo_falldown/4_New.avi')




