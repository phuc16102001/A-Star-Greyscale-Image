from MyImg import *
from constant import *
import math  #sqrt, fabs, abs
from time import * #sleep

def abs(x):
    if (x<0):
        return -x
    return x

def sign(x):
    if (x<0):
        return -1
    elif (x>0):
        return 1
    return 0

class Node:
    x = None
    y = None
    g = 0
    h = 0
    f = 0
    a = None
    parent = None

    def __init__(self,pos,a):
        self.x=pos[0]
        self.y=pos[1]
        self.a=a

    def print(self):
        print(self.x,self.y,self.a,self.g,self.h,self.f)

    def toStr(self):
        return ("%f %f %f %f %f %f\n"%(self.x,self.y,self.a,self.g,self.h,self.f))

    def euclidDistance(self,node):
        dx = self.x-node.x
        dy = self.y-node.y
        d = math.sqrt(dx**2+dy**2)
        return d

    def deltaA(self,node):
        return self.a-node.a
    
    def distanceTo(self,node):
        da = self.deltaA(node)
        d = self.euclidDistance(node)
        return d+(0.5*sign(da)+1)*abs(da)

    def calculateF(self):
        self.f = self.g+self.h

    def setParent(self,node):
        self.parent = node
        self.g = self.parent.g + self.parent.distanceTo(self)
        self.calculateF()

    def setH(self,h):
        self.h=h
        self.calculateF()

    def pos(self):
        return (self.x,self.y)


def convertPoint(raw):
    raw = raw[1:len(raw)-1]
    raw = raw.split(';')
    for i in range(len(raw)):
        raw[i] = int(raw[i])
    return tuple(raw)

def readInput(path):
    fin = open(path)
    data = fin.readlines()
    for i in range(len(data)):
        data[i] = data[i].replace('\n','')
    data[0]=convertPoint(data[0])
    data[1]=convertPoint(data[1])
    data[2]=int(data[2])
    fin.close()
    return (data[0],data[1],data[2])

def heuristic1(pos,goal):
    return pos.distanceTo(goal)

def heuristic2(pos,goal):
    return 0

def heuristic3(pos,goal):
    return pos.euclidDistance(goal)

def heuristic4(pos,goal):
    (px,py)=pos.pos()
    (gx,gy)=goal.pos()
    return abs(px-gx)+abs(py-gy)

def priority(node):
    return node.f

def getNeighboor(node):
    global img, m, nodeMat

    dx = [-1,-1,-1,0,0,1,1,1]
    dy = [-1,0,1,-1,1,-1,0,1]
    x = node.x
    y = node.y
    result = []
    for i in range(len(dx)):
        newX = x+dx[i]
        newY = y+dy[i]
        if (not(newX<0 or newY<0 or newX>=img.width or newY>=img.height)):
            neighboor = nodeMat[newY][newX]
            if (abs(node.deltaA(neighboor))<=m):
                result.append(neighboor)
    return result

def createNode(img):
    nodeMat = []
    for y in range(img.height):
        nodeRow = []
        for x in range(img.width):
            pos = (x,y)
            node = Node(pos,img.greyAt(pos))
            nodeRow.append(node)
        nodeMat.append(nodeRow)
    return nodeMat

def addQueue(parent,node,goal,hFunction):
    global queue, explored
    if (node in queue):
        oldG = node.g
        newG = parent.g+parent.distanceTo(node)
        if (newG<oldG):
            #node.print()
            node.setParent(parent)
            #node.print()
            #print("----")
        
    elif (not(node in explored)):
        node.setParent(parent)
        node.setH(hFunction(node,goal))
        queue.add(node)

def queuePrint():
    global queue
    for node in queue:
        node.print()

def findMin(queue,priority):
    v = None
    result = None
    for node in queue:
        if (v==None):
            result = node
            v = priority(result)
        else:
            newV = priority(node)
            if (newV<v):
                v = newV
                result = node
    return result
        
def run(hFunc,number):
    global img, start, end, m, explored, queue, nodeMat
    count = 0
    #newImg = img.copy("test%d.bmp"%(count))
    imgOut = img.copy("output%d.bmp"%(number))
    startNode = nodeMat[start[1]][start[0]]
    goalNode = nodeMat[end[1]][end[0]]
    addQueue(startNode,startNode,goalNode,hFunc)
    result = []
    while (len(queue)>0):
        node = findMin(queue,priority)
        #newImg.write(node.pos(),colorBlue)
        #newImg.save()
        #print("===========")
        #sleep(3)
        if (node==goalNode):
            #Traceback
            #pointOutput = open("point.txt",'w')
            #pointOutput.write("x y a g h f\n")
            while (node!=startNode):
                result.append(node)
                pos = node.pos()
                node.print()
                imgOut.write(pos,colorRed)
                node=node.parent
            result.append(startNode)
            result = result[::-1]
            #for node in result:
                #pointOutput.write(node.toStr())
            #pointOutput.close()
            break
        
        #Not goal
        queue.remove(node)
        explored.add(node)
        neighboor = getNeighboor(node)
        for i in range(len(neighboor)):
            addQueue(node,neighboor[i],goalNode,hFunc)
            pos = neighboor[i].pos()
            #newImg.write(pos,colorGreen)
            #newImg.save()
            #neighboor[i].print()
            
        #node.print()
        #queuePrint()
        #count+=1
        #newImg = newImg.copy("test%d.bmp"%(count))
        #print("=========")
    imgOut.save()
    imgOut.show()
    return (startNode,goalNode)
    
img = MyImg(defaultPath)
img.print()
start,end,m = readInput("input.txt")
nodeMat = createNode(img)
explored = set()
queue = set()
startNode, goalNode = run(heuristic2,1)
startNode.print()
goalNode.print()
