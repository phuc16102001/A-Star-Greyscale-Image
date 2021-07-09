from PIL import Image

class MyImg:

    path = None
    img = None
    width = None
    height = None

    def __init__(self,path):
        self.path = path
        self.img = Image.open(self.path)
        self.width, self.height = self.img.size

    def print(self):
        print("Path:",self.path)
        print("Width:",self.width)
        print("Height:",self.height)

    def at(self,pos):
        pixel = self.img.getpixel(pos)
        return pixel

    def show(self):
        self.img.show()

    def copy(self,des):
        self.img.save(des)
        return MyImg(des)

    def save(self):
        self.img.save(self.path)

    def write(self,pos,color):
        self.img.putpixel(pos,color)

    def greyAt(self,pos):
        pixel = self.at(pos)
        R = pixel[0]
        G = pixel[1]
        B = pixel[2]
        return (R+G+B)/3
