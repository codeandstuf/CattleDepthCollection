from asyncio.windows_events import NULL
from ctypes import pointer
import pyrealsense2 as rs
import time
from datetime import datetime
import cv2
import keyboard 
import numpy as np
from pynput.mouse import Listener


"""
This program records video when an object of a large enough size enters an area
Robert Kadlec 
9/23/2021
"""
class VideoCapture:
    x, y = 500, 360

    def __init__(self):
        global x,y
        x, y = 500, 360

    #used to run the camera how it was run in a Virginia Tech Trial
    def setupAuto(self, save_loc):
        #distance to ground / object that is constant
        #x  and y cords for point of intrest
        dist_to_ground = 3
        xCord = int(300)
        yCord = int(360)
        #how many pictures of each cow are to be taken
        #time between the pictures of the cow
        self.runCamera(dist_to_ground, xCord, yCord, save_loc)


    #when mouse is clicked
    def on_click(self, event, x1, y1, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            global x 
            global y
            x = x1
            y = y1

    #allows user to set POI, number of pics, time between pics
    def setupManual(self, save_loc):
        pipeline = rs.pipeline()
        #sets the configuration resolution and fps 
        config = rs.config()

        #sets up color and depth streams
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        pipeline.start(config)

        #align color frames to depth frame
        align_to = rs.stream.depth
        align = rs.align(align_to)

        #until enter is pressed
        while not keyboard.is_pressed('enter'):
            #get frames and align color with depth
            frames = pipeline.wait_for_frames()
            frames2 = align.process(frames)

            #get color and depth frame
            depth_frame = frames2.get_depth_frame()
            color_frame = frames2.get_color_frame()

            #convert to numpy array so they can be viewed using cv2
            depth_image = np.asanyarray(depth_frame.get_data())
            color_frames = np.asanyarray(color_frame.get_data())
            #apply a colormap 
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_HSV)

            #get depth to x y
            dep = depth_frame.get_distance(x,y)
            color_frames_new = color_frames.copy()
            str1 = 'X:' + str(x) + ' ' + 'Y:' +  str(y) + ' Depth:' + str(dep)

            #apply text for user
            cv2.putText(color_frames_new, str1, (100, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),2)
            cv2.circle(color_frames_new, (x,y), 5, (0,0,255),cv2.FILLED)
            #namedWindow allows to track mouse interaction
            cv2.namedWindow('Color Image')
            cv2.namedWindow('Depth Image')
            #display depth and color images
            cv2.imshow("Color Image",  color_frames_new)
            cv2.imshow("Depth Image",  depth_colormap)
            cv2.setMouseCallback("Color Image", self.on_click)
            cv2.setMouseCallback("Depth Image", self.on_click)
            #cv2.imshow("Color Image",  depth_image)
            cv2.waitKey()
        pipeline.stop()
        #distance to ground / object that is constant
        #x  and y cords for point of intrest
        dist_to_ground = dep
        xCord = int(x)
        yCord = int(y)
       
        cv2.destroyAllWindows()
        self.runCamera(dist_to_ground, xCord, yCord, save_loc)
    
    #records videos as cows walk under camera
    def runCamera(self, dist_to_ground, xCord, yCord, save_loc):
        #counts number of cows that pass through
        cowNum = 0
        while True:
            #start the pipeline (camera)
            # ...from Camera 1
            pipeline_1 = rs.pipeline()
            config_1 = rs.config()
            config_1.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
            config_1.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
            #sets up the camera settings and reccording file
            config_1.enable_record_to_file(save_loc + "Vidcow#_" + str(cowNum) + '_mdHMS_' + datetime.now().strftime("_%m_%d_%H_%M_%S")+  "__.bag")
            pipeline_record_profile = pipeline_1.start(config_1)
            device_record = pipeline_record_profile.get_device()
            device_recorder = device_record.as_recorder()

            #pause the recording until a cow is detected
            rs.recorder.pause(device_recorder)
            #start checking for cow
            while True: #while no cow is detectede

                #press e to end the program
                #this is important because it creates a trashed .bag file 
                #without this the last file won't save properly
                if keyboard.is_pressed('e'):
                    pipeline.stop()
                    pipeline = None
                    exit()

                # Waits for frames from camera
                frames = pipeline_1.wait_for_frames()
                #Retrieve the first depth frame, if no frame is found, return an empty frame instance.
                depth = frames.get_depth_frame()
    
                #checks the distance to xChord pixel and ychord pixel
                dist_to_center = float(depth.get_distance(xCord, yCord) )#int(width / 2), int(height / 2)

                print("The camera is facing an object " +
                      str(dist_to_center) + "meters away ")

                # checks if object is on point of intrest
                if(dist_to_center != 0 and dist_to_ground - dist_to_center > 1):
                    break
                
                #to avoid detecting the same cow twice wait 0.25 sec
                time.sleep(.25)

            #cow is detected, recording is resumed
            rs.recorder.resume(device_recorder)
            pipeline_1.wait_for_frames().keep()
            #increse cow count
            cowNum = cowNum + 1
        
            while True:  
                print("Recording")
                #Retrieve the first depth frame, if no frame is found, return an empty frame instance.
                frames_1 = pipeline_1.wait_for_frames()
                depth_1 = frames_1.get_depth_frame()

                #checks the distance to xChord pixel and ychord pixel
                dist_to_cow = float(depth_1.get_distance(xCord, yCord))

                #if cow has left, distance to object returns to distance to floor
                if(dist_to_cow != 0 and dist_to_ground - dist_to_cow < 0.5):
                    break
                time.sleep(.25)
            #unassigns all variables
            pipeline_1.stop()
            pipeline_1 = None
            config_1 = None

            print("Recording Stopped Reseting")

   