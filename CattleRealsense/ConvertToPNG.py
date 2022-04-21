#Author Robert Kadlec 2/3/2022
#this script uses rs-convert to convert .bag files inot PNG format
#Specify the input folder in the directory feild and the oputut directory in 
import os

class ConvertToPNG:

    def __init__(self):
        print('Starting Conversion')
        print('hello')

    def convert(self, inputFolder, outputFolder, toolsPath):
        #navigate to RealSense Tools
        os.chdir(toolsPath) ##PATH TO \\Intel RealSense SDK 2.0\\tools\

        commandIntro = 'cmd /c '
        commandPNG = 'rs-convert -i '
        command2 = ' -p '
        #iterate over files in directory

        for filename in os.listdir(inputFolder):
            if filename.endswith('.bag'):
                f = os.path.join(inputFolder, filename)
                print(filename)
                fullCommandPNG = commandIntro + commandPNG + f +" "  + command2 + outputFolder + filename 
                fullCommandCSV = commandIntro + 'rs-convert -i ' + f + ' ' + '-v ' + outputFolder + filename
                print(fullCommandCSV)
                #convert to PNG
                os.system(fullCommandPNG)
                #convert to CSV
                os.system(fullCommandCSV)
