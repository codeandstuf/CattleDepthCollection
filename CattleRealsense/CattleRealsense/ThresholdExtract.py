import cv2
import numpy as np
#import imutils
import os
import keyboard
import imutils
#folder to read from
inputFolder = "C:\\Users\\rdkbh\\OneDrive\\Desktop\\PNGOut\\"
#Folder to output threshold result
outputFolder = "C:\\Users\\rdkbh\\OneDrive\\Desktop\\FarmVisit7"


class ThresholdExtract:

    def __init__(self):
        global y1,y2, x1, x2, count
        y1,y2 = 0,0
        count = 0
    #when mouse is clicked
    def on_click(self, event, x1in, y1in, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print('clicked')
            global x1,y1, x2,y2, count
            if count == 0:
                y1 = y1in
                count+=1
            elif count < 2:
                y2 = y1in
                count+=1
            elif count < 3:
                x1 = x1in
                count+=1
            else:
                x2 = x1in

    def setCrop(self, inputFolder, outputFolder):
        
        while not keyboard.is_pressed('enter'):
            global count, y2
            count = 0
            fileList = os.listdir(inputFolder)

            cropFile = ''
            for file in fileList:
                if ("Depth" in file) and file.endswith('.png'):
                    cropFile = file
                    break
            #Load image
            Depth = cv2.imread(inputFolder + cropFile)
            cv2.namedWindow('Uncropped Image')
            cv2.putText(Depth, 'Click Upper, then Lower bound y cordinate', (10, 650), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255),2)
            cv2.putText(Depth, 'Click Left x then Right x. Then press ENTER', (10, 700), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255),2)
            cv2.imshow('Uncropped Image', Depth)
            cv2.setMouseCallback("Uncropped Image", self.on_click)
            cv2.waitKey()
            if (y2 == 0):
                y2 = Depth.shape[0]
            Depth = Depth[y1:y2, x1:x2]
            cv2.putText(Depth, 'press enter if done or r to set crop again', (0, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255),2)
            cv2.imshow('type d if done or r to set crop again', Depth)
            cv2.waitKey()
            #global y1, y2
        self.extract(y1, y2, x1, x2, inputFolder, outputFolder)



    def extract(self, y1Set, y2Set, x1set , x2set, inputFolder, outputFolder):
        #iterate over files in directory (inputFolder)
        #@param inputFolder must be directory containing only .png files
        for filename in os.listdir(inputFolder):
            if ("Depth" in filename) and filename.endswith('.png'):
                print(filename)

                #Load image
                Depth = cv2.imread(inputFolder + filename)
                cv2.imshow('Original Image', Depth)

                #crops image 
                #crop values should be set to inside of top rail 
                #this prevents errors in threshold seperation of rail
                Depth = Depth[y1Set:y2Set, x1set:x2set] #image crop


                #Convert RGB to HSV (Hue, Saturation, Value)
                hsvImage = cv2.cvtColor(Depth, cv2.COLOR_BGR2HSV)
                #show image (PRESS ANY KEY TO CONT)
                #cv2.imshow('HSV', hsvImage)

                #get h,s,v values
                h, s, v = hsvImage[:, :, 0], hsvImage[:, :, 1], hsvImage[:, :, 2]

                #creates a threshold using hue value
                (thresh, BW3) = cv2.threshold(h, 35, 255, cv2.THRESH_BINARY)
                cv2.imshow('H_Black and white', BW3)

                # Remove stuructures connected to the image border
                # find contours in the image and initialize the mask that will be
                cnts = cv2.findContours(BW3.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                mask = np.ones( BW3.shape[:2], dtype="uint8") * 255

                # Find contours and filter for largest contour
                # Draw largest contour onto a blank mask 
                mask = np.zeros(BW3.shape[:2], dtype=BW3.dtype)
                c = max(cnts, key = cv2.contourArea)
                cv2.drawContours(mask, [c], 0, (255), -1)
                largestContour = cv2.bitwise_and(BW3,BW3, mask= mask)
                #cv2.imshow('Largest Contour', largestContour)        
             
                #Fills contours
                #inverts binary image
                result = cv2.bitwise_not(np.invert(largestContour))
                contours, hierarchy = cv2.findContours(result,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                #Fills the contour
                cv2.drawContours(result,[contours[0]],0,255,-1)
                #cv2.imshow('Filled Result',  result)        
      
                #write result to file
                os.chdir(outputFolder)
                cv2.imwrite(filename, result)





