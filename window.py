import body_detect
import math as m
import threading
import time
import tkinter as tk
from collections import deque
import customtkinter as ck
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import PIL.Image
import PIL.ImageTk
import tensorflow as tf
from PIL import ImageTk
from sklearn.preprocessing import MinMaxScaler
import SourseDetecter
global Imgtk 

video_channel=["video 1", "video 2", "video 3 ","video 4","video 5 ","video 6 ","video 7 ","video 8 ","video 9 ","video 10 "]
class VideoApp(object):
    def __init__(self):
        global Imgtk,canvas,textbox
       
        Imgtk = None
        self.window = ck.CTk()
        self.window.title("Video Player")
        self.window.geometry('800x780')
        # create video capture object
        ck.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ck.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.classname = " "
        self.custom_font =("Times",30,'bold')
        # create canvas for video display
        self.canvas = ck.CTkCanvas(self.window, width=640, height=480)
        self.canvas.pack(anchor = "w",padx=10, pady=10 )
        self.running = False
        self.textbox1 = ck.CTkTextbox(master=self.window, width=250,height=50,fg_color="darkBlue",font=self.custom_font)
        self.textbox1.pack(side="left", padx=10, pady=10)
        # create text widget to display mediapipe results
        canvas = self.canvas
        textbox = self.textbox1
        self.frame(self.custom_font)
        try:
            print(self.classname)
        except:
            pass
        # create mediapipe pose detection object
        #self.mp_pose = mp.solutions.pose.Pose()
       
        # start the thread to read frames from the video stream
        
        try:
            print(self.classname)
        except:
            pass
        
        # start the main tkinter loop
        self.window.mainloop()
        #del self.mp_pose
    def compare(self,m,label_value_falldown,label_value_fine):   
        try:
                        #memory_test = [results ,frame ,self.vid ,self.label_value.falldown, self.label_value_fine, img, imgtk, self.canvas.image]
                        #self.label_value_falldown ,self.label_value_fine ,row_list= (calculate.calculate(results,mp_pose,lm,lmPose,h,w,frame_count,msec))
                        
                        
                        classname =" "
                        m=min(label_value_fine[0],label_value_falldown[0])
                        
                        #print(m,",",self.label_value_fine[0],",",self.label_value_falldown[0])
                        if ((label_value_falldown[0]) == m):
                            classname = ('falldown')
                            #self.classname = ('falldown')
                            
                            self.insert("1.0",classname+'\n')
                            
                        elif(label_value_fine[0] == m):
                            classname = ('fine')
                            #self.classname = ('fine')
                            
                            self.insert("1.0",classname+'\n')
                        

        except:
                        pass
                   
    def frame(self,custom_font):
        global textbox
        
        textbox = self.textbox1
        self.label = ck.CTkLabel(master=self.window, text="姿勢",font=custom_font)
        self.label.place(in_=self.window, relx=0.17, rely=0.75, anchor="c")
        self.btn_start = ck.CTkButton(master = self.window, text="start",width=220,height=50, command=self.start)
        self.btn_start.place(in_=self.window, relx=0.47, rely=0.82, anchor="c")
        self.btn_start.pack(side="left", padx=10, pady=10)
        self.btn_stop = ck.CTkButton(master = self.window, text="stop", width=220,height=50, command=self.stop)
        self.btn_stop.place(in_=self.window, relx=0.91, rely=0.82, anchor="c")
        self.btn_stop.pack(side="left", padx=10, pady=10)
        def optionmenu_callback(choice):
            
            print("optionmenu dropdown clicked:", choice)
            s = SourseDetecter.SourseDetecter()
            video_path = s.Get_video(choice)

            return (video_path) 
        self.optionmenu_1 = ck.CTkOptionMenu(master=self.window,
                                       values=["video 1", "video 2", "video 3 ","video 4","video 5 ","video 6 ","video 7 ","video 8 ","video 9 ","video 10 "],
                                       command=optionmenu_callback)
        self.optionmenu_1.pack(padx=20, pady=10)
        self.optionmenu_1.place(in_=self.window, relx=1, rely=0.03, anchor="ne")
        self.optionmenu_1.set("videoOption")  # set initial value
        try:
            print(Imgtk) 
            self.canvas.itemconfig(self.canvas.create_image(0, 0, image=Imgtk, anchor=tk.NW))
            self.canvas.image = Imgtk
        except ValueError as err:
            print(err)
    def textbox(self,imgtk):
            global Imgtk
            Imgtk = body_detect.imgtk  
            print(Imgtk)
            self.itemconfig(self.create_image(0, 0, image=Imgtk, anchor=tk.NW))
            self.image = Imgtk         
    def cavas(self,imgtk):
            global Imgtk
            Imgtk = body_detect.imgtk  
            print(Imgtk)
            self.itemconfig(self.create_image(0, 0, image=Imgtk, anchor=tk.NW))
            self.image = Imgtk        
    def __str__(self):
            print("window")     
    def start(self):
        self.running = True
        print("start")
    def stop(self):
        self.running = False    
        print("stop")
        

    #def MarkPose(self,result,img):

app = VideoApp()


    
       



