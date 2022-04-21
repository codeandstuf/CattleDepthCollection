 
# Depth Data Collection Using Intel D435 Depth Camera
This extension provides tools to easily collect depth and color data from a top view of cattle

# WARNING
Picturecapture, Videocapture, and BAGtoPNG can only be run on a Windows platform. Thresholding can be run on Windows or Mac.

## Requierments Windows
- python (any version since 3.6 to 3.9)
- code editor (Visual Studio Code is what I reccomend)
- Realsense SDK https://www.intelrealsense.com/sdk-2/
- Realsense SDK Instrucitons for Windows https://www.youtube.com/watch?v=EOJHsNIayio&ab_channel=IntelRealSense
## Requierments Mac
- python (any version since 3.6 to 3.9)
- code editor (Visual Studio Code is what I reccomend)




# Windows Instructions
## pip install 
```
pip install CattleRealsense==0.1.7
```
## How to collect picutres 

```
from CattleRealsense.PictureCapture import PictureCapture as ps

#Instance of a PictureCapture
pictureTake = ps()

#location to save pictures
#make sure to convert all \ to \\
#example, if you would like to save the picutres to a folder in your desktop, saveLocaitonPath will look something like
saveLocationPath = "C:\\Users\\johndoe\\Desktop\\BAG\\" #files will be saved in a folder named BAG 

#Lets user set the point of intrest, depth, number of picutres, and time inbetween picutres
#picture colleciton will start after setup is complete
pictureTake.setupManual(saveLocationPath)
```
When this is running you will be shown a depth and color pciutre from your camera. Click a location on either picutre to set a point of intrest. After clicking type r to refresh the image. When saticified with point of intrest location hit enter on your keyboard.
## Alternative approaches to starting picture collection

to use the same setting as used by Virginia Tech (x = 500, y = 360, distance_to_ground = 3 meters, 
                                                  num_of_picutres = 10, time_between_pics = 0.15s
                                                  save_location = foulder where code is)
```
from CattleRealsense.PictureCapture import PictureCapture as ps

pictureTake = ps()
pictureTake.setupAuto(saveLocationPath)
```
to run custom collection without going through the setup process
```
from CattleRealsense.PictureCapture import PictureCapture as ps

#Instance of a PictureCapture
pictureTake = ps()
#fill in parameters to match desired 
pictureTake.runCamera(dist_to_ground, xCord, yCord, number_of_pics, sec_between_pics, save_location):
```
All recording processes will stop when user ends program 

## How to collect videos 
this is the same process as Picture Collection but without number_of_pics, sec_between_pics
```
from CattleRealsense.VideoCapture import VideoCapture as vc

#location to save videos
#make sure to convert all \ to \\
#example, if you would like to save the picutres to a folder in your desktop, saveLocaitonPath will look something like
saveLocationPath = "C:\\Users\\johndoe\\Desktop\\BAG\\" #files will be saved in a folder named BAG 

videoTake = vc()

#to setup manually
videoTake.setupManual(saveLocationPath)
```
## Alternative approaches to starting video collection

to use the same setting as used by Virginia Tech
```
from CattleRealsense.PictureCapture import PictureCapture as ps

#Instance of a PictureCapture
videoTake = vc()
videoTake.setupAuto(saveLocationPath)
```
to run collection without giong through the setup process
```
from CattleRealsense import PictureCapture as ps

#Instance of a PictureCapture
videoTake = vc()
#fill in parameters to match desired 
videoTake.runCamera(self, dist_to_ground, xCord, yCord, save_loc):
```

# How to convert .bag to .png
During data collection all files will be saved as .bag. This makes it hard to use. To convert the .bag files to .png follow the following code

```
from CattleRealsense.ConvertToPNG import ConvertToPNG as convert

con = conver()

#inputFolder = Path to .bag folder 
#outputFolder = path to save .png created
#toolsPath = path where  \\Intel RealSense SDK 2.0\\tools\ is saved
#toolspath will likely be "C:\\Program Files (x86)\\Intel RealSense SDK 2.0\\tools\\"

#run the conversion program
con.convert(inputFolder, outputFolder, toolsPath):
```

## How to threshold png files
To get an accurate threshold it is imporant to crop the image horizontally to the smallest area needed.
This prevents the surrounding objects from interfereing. 
When running this program the first picutre in from inputFolder will be shown.
 - You should click the upper bound, lower bound, left bount, right bound in that order.
 - After clicking the mouse 4 times hit enter on your keyboard
 - The cropped photo will appear. If you are happy with the result hit enter again to run thresholding.
 - If you would like to select new crop values type r
```
from CattleRealsense.ThresholdExtract import ThresholdExtract as te

extract = te()

#inputFolder = path to .png files
#outputFolder = path to save threshold results
extract.setCrop(inputFolder, outputFolder)
```

# Mac Instructions 

## Setting up Visual Studio Code
Follow these instructions if you would like to use Visual Studio Code (VSC)
 - download VSC
 - open VSC click file --> new file
 - click 'select a language' and chose python
 - type command s and enter desired name followed by .py
 - type ```print('Hello World')``` into the file. save the file
 - on the top toolbar select Run --> Run Without Debugging 
 - if you are asked to install an extension do so. The top option from the search bar should work fine. run the program again
 - if 'Hello World' is printed in the terminal you are good to continue. 

## Intalling CattleRealsense
 In the terminal type ```python3 -m pip install CattleRealsense==0.1.7``` or ```sudo python3 -m pip install CattleRealsense==0.1.7```

## How to threshold png files
To get an accurate threshold it is imporant to crop the image horizontally to the smallest area needed.
This prevents the surrounding objects from interfereing. 
When running this program the first picutre in from inputFolder will be shown.
 - You should click the upper bound, lower bound, left bount, right bound in that order.
 - After clicking the mouse 4 times hit enter on your keyboard
 - The cropped photo will appear. If you are happy with the result hit enter again to run thresholding.
 - If you would like to select new crop values type r
```
from CattleRealsense.ThresholdExtract import ThresholdExtract as te

extract = te()

#inputFolder = saveLocationPathMac = "X: /Users/username/Desktop" #if files are on desktop
#outputFolder = path to save threshold results
extract.setCrop(inputFolder, outputFolder)
```

