import os
import threading
import time
import body_detect
import control_center
video_path = None
video_dict={"video 1":'2', "video 2":'3', "video 3 ":'4',"video 4":'5',"video 5 ":'6',"video 6 ":'7',"video 7 ":'8',"video 8 ":'9',"video 9 ":'10',"video 10 ":'11'

}
class SourseDetecter(object):
    def __init__(self):
        pass
    def Get_video(self,object):
        
        video_path = "D:/user/Desktop/TrainingVideo_falldown/"+video_dict[object]+"_New.avi"
        if os.path.exists(video_path):
            print(video_path)
            #control_center.control_center.get_video_address(video_path)
            self.thread1 = threading.Thread(target=body_detect.body_detect, args=(video_path,))
            self.thread1.start()
            time.sleep(1)
        else:

            raise FileNotFoundError("Not is File")    
__all__ = ['SourseDetecter']   

