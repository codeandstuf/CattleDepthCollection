
from CattleRealsense.PictureCapture import PictureCapture as ps
from CattleRealsense.ConvertToPNG import ConvertToPNG as conPNG
from CattleRealsense.ThresholdExtract import ThresholdExtract as te
from CattleRealsense.VideoCapture import VideoCapture as vc
path_to_BAG_save_file = "C:\\Users\\JohnDoe\\OneDrive\\Desktop\\testSaver\\BAG\\"
path_to_PNG_save_file = "C:\\Users\\JohnDoe\\OneDrive\\Desktop\\testSaver\\PNG\\"
extracted = 'C:\\Users\\JohnDoe\\OneDrive\\Desktop\\testSaver\\CowThreshold\\'
toolsPath = "C:\\Program Files (x86)\\Intel RealSense SDK 2.0\\tools\\"

#capture pictures
pictureTake = ps()
pictureTake.setupManual(path_to_BAG_save_file)

videoTake = vc()
videoTake.setupManual(path_to_BAG_save_file)

#convet bags to png
converter = conPNG()
converter.convert(path_to_BAG_save_file, path_to_PNG_save_file, toolsPath)

#Get threshold
thresh = te()
thresh.setCrop(path_to_PNG_save_file, extracted)
