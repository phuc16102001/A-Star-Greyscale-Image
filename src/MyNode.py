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

from MyMath import *

class Node:
    #========================Attribute=========================
    x = None        #x-coordinate of the node
    y = None        #y-coordinate of the node
    g = 0           #g(node) is the cost from the start
    h = 0           #h(node) is the heuristic cost to goal
    f = 0           #f(node)=g(node)+h(node)
    a = None        #a(node)=greyscale(x,y)
    parent = None   #parent node of the current node

    #========================Method=========================
    #Construction for node
    #Input: pos=Tuples(x,y); a=greyscale(float/int)
    def __init__(self,pos,a):
        self.x=pos[0]
        self.y=pos[1]
        self.a=a

    #Print the information of a node
    #Output: To screen (x,y,a,g,h,f)
    def printInfo(self):
        print(self.x,self.y,self.a,self.g,self.h,self.f)

    #Cast the node to string
    #Output: string("x y a g h f")
    def toStr(self):
        return ("%f %f %f %f %f %f\n"%(self.x,self.y,self.a,self.g,self.h,self.f))

    #Get the euclid distance (diagonal distance) between the current to another node
    #Input: node = Node
    #Output: euclid distance from self to node = (int/float)
    def euclidDistance(self,node):
        dx = self.x-node.x
        dy = self.y-node.y
        d = math.sqrt(dx**2+dy**2)
        return d

    #Get the difference of greyscale value when move from current to another node
    #Input: node = Node
    #Output: difference of greyscale a(self)-a(node)
    def deltaA(self,node):
        return self.a-node.a
    
    #Get the cost from the current when move to the parameter node
    #Input: node = Node
    #Output: the cost for move from current to the parameter node
    def distanceTo(self,node):
        da = self.deltaA(node)
        d = self.euclidDistance(node)
        return d+(0.5*sign(da)+1)*abs(da)

    #Calculate the f(self)
    def calculateF(self):
        self.f = self.g+self.h

    #Set the parent node of current node
    def setParent(self,node):
        self.parent = node 
        self.g = self.parent.g + self.parent.distanceTo(self)
        self.calculateF()

    #Set the heuristic value for current node
    def setH(self,h):
        self.h=h
        self.calculateF()

    #Get the current position
    #Output: Tuple(x,y)
    def pos(self):
        return (self.x,self.y)