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

#=============================Library=============================
from MyImg import *
from constant import *
from MyMath import *
from MyNode import *

#=============================Heuristic function=============================
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

#=============================Utils function=============================

#Convert from format "(x;y)" to tuple(x,y)
#Input: raw = String in format "(x;y)"
#Output: Tuple(x,y)
def convertPoint(raw):
    raw = raw[1:len(raw)-1]
    raw = raw.split(';')
    for i in range(len(raw)):
        raw[i] = int(raw[i])
    return tuple(raw)


#Read the input file to get data
#Input: path = String of file path
#Output: Tuple(start,end,m) with start=Tuple(x,y) and end=Tuple(x,y)
def readInput(path):
    fin = open(path)
    data = fin.readlines()
    for i in range(len(data)):
        data[i] = data[i].replace('\n','')
    data[0]=convertPoint(data[0])   #Start point
    data[1]=convertPoint(data[1])   #End point
    data[2]=int(data[2])            #Value m
    fin.close()
    return (data[0],data[1],data[2])

#The priority function to create heap
#Input: node = Node
#Output: Value of priority
def priority(node):
    return node.f

#Get all the neighboor node (adjacent, |deltA|<=m)
#Input: node = Node
#Output: list of Node 
def getNeighboor(nodeMat, m, node):
    dx = [-1,-1,-1,0,0,1,1,1]
    dy = [-1,0,1,-1,1,-1,0,1]
    x = node.x
    y = node.y
    width = len(nodeMat)
    height = len(nodeMat[0])

    result = []
    for i in range(len(dx)):
        newX = x+dx[i]
        newY = y+dy[i]
        if (not(newX<0 or newY<0 or newX>=width or newY>=height)):
            neighboor = nodeMat[newY][newX]
            if (abs(node.deltaA(neighboor))<=m):
                result.append(neighboor)
    return result

#Create nodes matrix from an image
#Input: img = MyImg
#Output: list of list Node (matrix Node)
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

def addNodeToQueue(queue,node):
    pass

#Add a node to the queue
#Input: parent, node, goal, hFunction = Node, Node, Node, Pointer to a float-return function
#Description: Add [node] to queue whose [parent] and [goal] with the heuristic function [hFunction]
def checkNode(queue,explored,parent,node,goal,hFunction):

    if (node in queue):
        oldG = node.g
        newG = parent.g+parent.distanceTo(node)
        if (newG<oldG):
            node.setParent(parent)
    elif (not(node in explored)):
        node.setParent(parent)
        node.setH(hFunction(node,goal))
        queue.add(node)

#Print the queue (For debug only)
def queuePrint():
    global queue
    for node in queue:
        node.printInfo()

#Function to find the min Node in the queue with the priority function
#Input: queue, priority = Queue, Pointer to a float-return function
#Output: minNode = Node
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
        
#Running function
#Input: img, hFunc, number = MyImage, Pointer to float-return function, int
#Output: img, path, cost, nTouchNode = MyImg, list of Node, float, int
def run(img, hFunc, startPos, endPos, m, number):
    
    #Explored and queue set
    explored = set()
    queue = set()

    #Copy into a new image
    imgOut = img.copy("output%d.bmp"%(number))
    nodeMat = createNode(img)
    
    #Get the start and goal node
    startNode = nodeMat[startPos[1]][startPos[0]]
    goalNode = nodeMat[endPos[1]][endPos[0]]
    
    #Add the startNode to queue
    checkNode(queue,explored,startNode,startNode,goalNode,hFunc)

    #If the queue is not empty
    while (len(queue)>0):
        #Pop the highest priority out (lowest Node.f)
        node = findMin(queue,priority)

        #If we found the goal (end searching)
        if (node==goalNode):
            #Traceback
            print("FOUND")
            result = []
            while (node!=startNode):
                result.append(node)
                imgOut.write(node.pos(),colorRed)
                node=node.parent
            result.append(startNode)
            result = result[::-1]
            imgOut.save()                                                       #Save the image
            imgOut.show()                                                       #Open
            return result
        
        #Not goal
        queue.remove(node)                                              #Remove the poped
        explored.add(node)                                              #Add to explored set
        neighboor = getNeighboor(nodeMat,m,node)                        #Get list of node that can move
        for i in range(len(neighboor)):                                 #For each node
            checkNode(queue,explored,node,neighboor[i],goalNode,hFunc)  #Add that neighboor to queue if it better
    return None
    
#=============================Main driven=============================
def main():
    #Input
    img = MyImg(defaultPath)
    img.printInfo()
    startPos, endPos, m = readInput(inputPath)

    #Get result
    result = run(img, heuristic2, startPos, endPos, m, 1)
    if (result!=None):
        result[0].printInfo()
        result[-1].printInfo()

if __name__=="__main__":
    main()