#import tkinter as tk
import threading
import cv2
import window
import customtkinter as ck
import tensorflow as tf
from PIL import ImageTk
import mediapipe as mp
import time
import pandas as pd
import numpy as np
from collections import deque
from sklearn.preprocessing import MinMaxScaler
import math as m
import PIL.Image, PIL.ImageTk
frame_array = []
frame_array = []
duration_array = []
sk_array = []
#count = 0
frame_check = 0  
row_list = []
scaler = MinMaxScaler(feature_range=(-1, 1))
class Falldetect(object):
    def __init__(self):
          pass
    def calculate(results,mp_pose,lm,lmPose,h,w,frame_count,msec):
            global frame_array, duration_array, sk_array, frame_check, scaler,row_list
            count = 0
            # results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width
            if results.pose_landmarks:
                l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x*w)
                l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y*h)

                r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x*w)
                r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y*h)

                l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x*w)  # 髖關節
                l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y*h)

                r_hip_x = int(lm.landmark[lmPose.RIGHT_HIP].x*w)
                r_hip_y = int(lm.landmark[lmPose.RIGHT_HIP].y*h)

                l_knee_x = int(lm.landmark[lmPose.LEFT_KNEE].x*w)
                l_knee_y = int(lm.landmark[lmPose.LEFT_KNEE].y*h)

                r_knee_x = int(lm.landmark[lmPose.RIGHT_KNEE].x*w)
                r_knee_y = int(lm.landmark[lmPose.RIGHT_KNEE].y*h)

                l_ankle_x = int(lm.landmark[lmPose.LEFT_ANKLE].x*w)
                l_ankle_y = int(lm.landmark[lmPose.LEFT_ANKLE].y*h)

                r_ankle_x = int(lm.landmark[lmPose.LEFT_ANKLE].x*w)
                r_ankle_y = int(lm.landmark[lmPose.LEFT_ANKLE].y*h)
                # dis = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

                sk1 = np.array(([l_shldr_y, r_shldr_y, l_hip_y, r_hip_y,
                               l_knee_y, r_knee_y, l_ankle_y, r_ankle_y]), dtype=float)
                # sk = np.array(([r_shldr,l_shldr],[l_hip,r_hip]),dtype=float)

                count += 1
                if count == 1:  # 存第一組數值
                    l_shldr = np.array([l_shldr_x, l_shldr_y])
                    r_shldr = np.array([r_shldr_x, r_shldr_y])
                    l_hip = np.array([l_hip_x, l_hip_y])
                    r_hip = np.array([r_hip_x, r_hip_y])
                    l_knee = np.array([r_knee_x, r_knee_y])
                    r_knee = np.array([l_knee_x, l_knee_y])
                    l_ankle = np.array([l_ankle_x, l_ankle_y])
                    r_ankle = np.array([r_ankle_x, r_ankle_y])
                Angle0 = ((findAngle(l_shldr[0], l_shldr[1], l_shldr_x, l_shldr_y)+findAngle(l_hip[0], l_hip[1], l_hip_x, l_hip_y)),
                          (findAngle(r_shldr[0], r_shldr[1], r_shldr_x, r_shldr_y)+findAngle(r_hip[0], r_hip[1], r_hip_x, r_hip_y)))

                Angle1 = ((findAngle(l_hip[0], l_hip[1], l_hip_x, l_hip_y)+findAngle(l_knee[0], l_knee[1], l_knee_x, l_knee_y)),
                          (findAngle(r_hip[0], r_hip[1], r_hip_x, r_hip_y)+findAngle(r_knee[0], r_knee[1], r_knee_x, r_knee_y)))
                # print("frame_count",".",frame_count,":",Angle)
                # print(Angle0,"|||",Angle1,"|||",fall_speed.mean())
                dis = findDistance(
                    l_hip_x, l_hip_y, r_hip_x, r_hip_y, l_ankle_x, l_ankle_y, r_ankle_x, r_ankle_y)
                Angle = np.mean(np.abs(Angle0))
                Angle_lower_body = np.mean(np.abs(Angle1))

                
                if frame_count % 5 == 1:  # 數1到5的幀數
                    frame_array = np.array(int(frame_count), dtype=np.int32)
                    duration_array = np.array((msec*0.001), dtype=np.float32)
                    sk_array = sk1
                    frame_check += 1

                elif (frame_count % 5 == 0) & (frame_count > 1) & (frame_check > 0):

                    frame_array1 = np.array(int(frame_count), dtype=np.int32)
                    duration_array1 = np.array((msec*0.001), dtype=np.float32)
                    sk_array1 = sk1
                    duration = duration_array1 - duration_array

                    fall_speed = np.abs((sk_array1-sk_array)/duration)

                    row = list(np.array(Angle0))+list(np.array(Angle1))+list(np.array(fall_speed)) + list(np.array((sk_array1-sk_array)/duration)) + list([dis])
                    row = np.array(row).reshape(-1, 1)
                    row = pd.DataFrame(scaler.fit_transform(row))
                    
   
                    row_list = np.append(row_list, row)        
                    if (len(row_list) > 63):
                        model = tf.keras.models.load_model('fall_model(43).h5')
                    else:
                        model = tf.keras.models.load_model('fall_model(42).h5')
                    label_layer = model.layers

                    # 將輸出張量作為輸入編譯一個新的模型
                    label_model = tf.keras.models.Model(
                            inputs=model.input, outputs=model.output) 
                    if len(row_list) < 63:
                        
                        label_value = label_model.predict(
                            np.array([row]*1).reshape(1, 1, 21))
                    if len(row_list) > 63:
                        
                        row_list = deque(row_list, maxlen=84)
                        label_value = label_model.predict(
                            np.array([row_list]).reshape(1, 4, 21))
               
                    try:
                        
                        return label_value[0, [0]] ,label_value[0, [1]]
                        
                    except:
                        pass
'''def __str__(self):
            print("control_center")'''            
def findAngle(x1, y1, x2, y2):
    while True:
        theta = m.acos(((y2 - y1)*(-y1)) /
                       (m.sqrt((x2-x1)**2+(y2 - y1)**2)*y1+0.0000000001))
        degree = int(180/(m.pi*theta))
        return degree  
def findDistance(l_hip_x, l_hip_y, r_hip_x, r_hip_y, l_ankle_x, l_ankle_y, r_ankle_x, r_ankle_y):
    hip = [(l_hip_x+l_hip_x)*0.5, (l_hip_y+r_hip_y)*0.5]
    ankle = [(l_ankle_x+l_ankle_x)*0.5, (l_ankle_y+r_ankle_y)*0.5]
    dis = m.sqrt((hip[0]-ankle[0])**2+(hip[1]-ankle[1])**2)
    return dis 



if __name__ == '__main__':
    Falldetect()
    #'D:/user/Desktop/TrainingVideo_falldown/3_New.avi'

