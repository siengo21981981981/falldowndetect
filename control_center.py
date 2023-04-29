import threading

import window
import customtkinter as ck
import body_detect
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


class control_center(object):
    def __init__(self):
        
        self.thread = threading.Thread(target=window.VideoApp)
        #self.thread1 = threading.Thread(target=body_detect.body_detect, args=("D:/user/Desktop/TrainingVideo_falldown/3_New.avi",))
        
        #self.thread1.daemon = True
        self.thread.start()
        #self.thread1.start()
        time.sleep(1)
        result = self.thread.join()
        print(result)
            
        
        
        result = self.thread1.join()
         
    '''def get_video_address(video_sourse):
        return video_sourse '''
        

if __name__ == '__main__':
    
    control_center()
    
