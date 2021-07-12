######################################
#                                    #
# Project name: A* for greyscale img #
# Author: Do Vuong Phuc              #
# Author: Hoang Nhu Thanh            #
# Date: 07/12/2021                   #
# Contact: phuc16102001@gmail.com    #
# * Please do not copy the source *  #
#                                    #
######################################

from PIL import Image

class MyImg:
    #========================Attribute=========================
    path = None     #Path to the image
    img = None      #The image data (Image from PIL)
    width = None    #Width of the image
    height = None   #Height of the image

    #========================Method============================
    #Create an image class with the path file
    def __init__(self,path):
        self.path = path
        self.img = Image.open(self.path)
        self.width, self.height = self.img.size

    #Print the image information
    def printInfo(self):
        print("Path:",self.path)
        print("Width:",self.width)
        print("Height:",self.height)

    #Get the pixel at a position
    #Input: Tuples(x,y)
    #Output: Tuples(R,G,B,A) with A is optional
    def at(self,pos):
        pixel = self.img.getpixel(pos)
        return pixel

    #Use the default application to open the image
    def show(self):
        self.img.show()

    #Create a new image with the destination
    #Input: The destination string
    #Output: The class point to the new image
    def copy(self,des):
        self.img.save(des)
        return MyImg(des)

    #Override the image with current data
    def save(self):
        self.img.save(self.path)

    #Write a pixel at position (x,y) and the color
    #Input: pos=Tuples(x,y), color=Tuples(R,G,B)
    def write(self,pos,color):
        self.img.putpixel(pos,color)

    #Get the grey pixel at the position(x,y)
    #Input: pos=Tuples(x,y)
    #Output: grey value
    def greyAt(self,pos):
        pixel = self.at(pos)
        R = pixel[0]
        G = pixel[1]
        B = pixel[2]
        return (R+G+B)/3