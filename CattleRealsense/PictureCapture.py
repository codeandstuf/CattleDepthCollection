import pyrealsense2 as rs
import time
from datetime import datetime
import cv2
import keyboard 
import numpy as np
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

"""
This program takes depth pictures when an object of a large enough size enters an area
Robert Kadlec 
9/23/2021
"""
class PictureCapture:
    x, y = 500, 360

    def __init__(self):
        global x,y
        x, y = 500, 360

    #used to run the camera how it was run in a Virginia Tech Trial
    def setupAuto(self, save_loc):
        #distance to ground / object that is constant
        #x  and y cords for point of intrest
        dist_to_ground = 3
        xCord = int(500)
        yCord = int(360)
        #how many pictures of each cow are to be taken
        number_of_pics = 10
        #time between the pictures of the cow
        sec_between_pics = .15
        self.runCamera(dist_to_ground, xCord, yCord, int(number_of_pics), int(sec_between_pics), save_loc)


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
            str1 = 'X:' + str(x) + ' ' + 'Y:' +  str(y) + ' Depth:' + str(round(dep, 3)) + 'm'

            #apply text for user
            cv2.putText(color_frames_new, str1, (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),2)
            cv2.putText(color_frames_new, 'Press r to refresh or enter when done', (50, 700), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255),2)
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
        #how many pictures of each cow are to be taken
        ROOT = tk.Tk()
        ROOT.withdraw()
        # the input dialog
        USER_INP = simpledialog.askstring(title="User Input",
                                          prompt="Enter number of picutres per cow:")

        number_of_pics = USER_INP
        #time between the pictures of the cow
        ROOT.withdraw()
        # the input dialog
        USER_INP2 = simpledialog.askstring(title="User Input",
                                          prompt="Enter time delay (sec) between each picutre:")
        sec_between_pics = USER_INP2
        print(number_of_pics)
        print(sec_between_pics)
        cv2.destroyAllWindows()
        self.runCamera(dist_to_ground, xCord, yCord, int(number_of_pics), float(sec_between_pics), save_loc)

    #starts camera recording process
    def runCamera(self, dist_to_ground, xCord, yCord, number_of_pics, sec_between_pics, save_loc):
        pipeline = rs.pipeline()
        #sets the configuration resolution and fps 
        config = rs.config()
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        pipeline.start(config)
        cowCount = 0
        while True:
            cow = False
            while not cow: #while no cow is detected
                #gets the distance to center pixel
                frame = pipeline.wait_for_frames()
                #Retrieve the first depth frame, if no frame is found, return an empty frame instance.
                depth = frame.get_depth_frame()
                #checks the distance to xChord pixel and yChord pixel
                dist_to_center = float(depth.get_distance(xCord, yCord))

                # if first loop dist_to_center_previous set to dist_to_center
                # checks for distance change
                if(dist_to_center != 0 and dist_to_ground - dist_to_center > 1):
                    cow = True

                #prints distance information
                print("The camera is facing an object " +
                      str(dist_to_center) + "meters away ")
                #wait 1/4 sec
                time.sleep(.25)
            #set cow to false to allow a while loop
            cow = False
            cowCount = cowCount + 1
            i = 0
            while not cow:  
                print("Cow Detected")
                #waits for frames
                while (i < number_of_pics):
                    saver = rs.save_single_frameset(save_loc + "cow#_"  + str(cowCount) + "_pic#_" + str(i) + '_mdHMS_' + datetime.now().strftime("_%m_%d_%H_%M_%S")+  "__")
                    saver.process(frame)
                    time.sleep(sec_between_pics)
                    frame = pipeline.wait_for_frames()
                    i=i + 1

                frames = pipeline.wait_for_frames()
                #Retrieve the first depth frame, if no frame is found, return an empty frame instance.
                depth = frames.get_depth_frame()

                #checks the distance to xChord pixel and ychord pixel
                dist_to_center = float(depth.get_distance(xCord, yCord))

                print(str(dist_to_center))
                #checks if cow left
                if(dist_to_center != 0 and dist_to_ground - dist_to_center < .5):
                    cow = True
                time.sleep(0.20)
