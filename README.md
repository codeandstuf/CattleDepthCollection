 
# Depth Data Collection Using Intel D435 Depth Camera
This extension provides tools to easily collect depth and color data from a top view of cattle

## Requierments
- python (any version since 3.6 or newer)
- code editor (Visual Studio Code is what I reccomend)
- Realsense SDK https://www.intelrealsense.com/sdk-2/
- Realsense SDK Instrucitons for Windows https://www.youtube.com/watch?v=EOJHsNIayio&ab_channel=IntelRealSense
- Realsense SDK Instrucitons for Mac https://dev.intelrealsense.com/docs/macos-installation-for-intel-realsense-sdk

#pip install 
```
pip install CattleDepthCollection==0.1.0
```

# How to collect picutres 

```
from CattleRealsense import PictureCapture as ps

#Instance of a PictureCapture
pictureTake = ps()

#location to save pictures
#make sure to convert all \ to \\
#example, if you would like to save the picutres to a folder in your desktop, saveLocaitonPath will look something like
saveLocationPath = "C:\\Users\\johndoe\\Desktop\\BAG\\" #WINDOWS
saveLocationPathMac = "X: /Users/username/Desktop" #MAC

#files will be saved in a folder named BAG 

#Lets user set the point of intrest, depth, number of picutres, and time inbetween picutres
#picture colleciton will start after setup is complete
pictureTake.setupManual(saveLocationPath)

```
When this is running you will be shown a depth and color pciutre from your camera. Click a location on either picutre to set a point of intrest. After clicking type r to refresh the image. When saticified with point of intrest location hit enter on your keyboard.
## Alternative approaches to starting picture collection

to use the same setting as used by Virginia Tech
```
from CattleRealsense import PictureCapture as ps

#Instance of a PictureCapture
pictureTake = ps()
pictureTake.setupAuto(saveLocationPath)
```
to run collection without giong through the setup process
```
from CattleRealsense import PictureCapture as ps

#Instance of a PictureCapture
pictureTake = ps()
#fill in parameters to match desired 
pictureTake.runCamera(dist_to_ground, xCord, yCord, number_of_pics, sec_between_pics, save_location):
```

All recording processes will stop when user ends program 

# How to collect videos 
this is the same process as Picture Collection but without number_of_pics, sec_between_pics
```
from CattleRealsense import VideoCapture as vc

videoTake = vc()

#to setup manually
videoTake.setupManual(saveLocationPath)
```
## Alternative approaches to starting picture collection

to use the same setting as used by Virginia Tech
```
from CattleRealsense import PictureCapture as ps

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
from CattleRealsense import ConvertToPNG as convert

con = conver()

#inputFolder = Path to .bag folder 
#outputFolder = path to save .png created
#toolsPath = path where  \\Intel RealSense SDK 2.0\\tools\ is saved
#toolspath will likely be "C:\\Program Files (x86)\\Intel RealSense SDK 2.0\\tools\\"

#run the conversion program
con.convert(inputFolder, outputFolder, toolsPath):
```

# How to threshold png files
To get an accurate threshold it is imporant to crop the image horizontally to the smallest area needed.
This prevents the surrounding objects from interfereing. 

```
from CattleRealsense import ThresholdExtract as te

extract = te()

#inputFolder = path to .png files
#outputFolder = path to save threshold results
extract.setCrop(inputFolder, outputFolder)
```

