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

#=============================Utils function=============================
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
    data[0]=convertPoint(data[0])   #Start point
    data[1]=convertPoint(data[1])   #End point
    data[2]=int(data[2])            #Value m
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
            node.setParent(parent)
    elif (not(node in explored)):
        node.setParent(parent)
        node.setH(hFunction(node,goal))
        queue.add(node)

def queuePrint():
    global queue
    for node in queue:
        node.printInfo()

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
    imgOut = img.copy("output%d.bmp"%(number))
    startNode = nodeMat[start[1]][start[0]]
    goalNode = nodeMat[end[1]][end[0]]
    addQueue(startNode,startNode,goalNode,hFunc)
    result = []
    while (len(queue)>0):
        node = findMin(queue,priority)
        if (node==goalNode):
            #Traceback
            while (node!=startNode):
                result.append(node)
                pos = node.pos()
                node.printInfo()
                imgOut.write(pos,colorRed)
                node=node.parent
            result.append(startNode)
            result = result[::-1]
            break
        
        #Not goal
        queue.remove(node)
        explored.add(node)
        neighboor = getNeighboor(node)
        for i in range(len(neighboor)):
            addQueue(node,neighboor[i],goalNode,hFunc)
            pos = neighboor[i].pos()
    imgOut.save()
    imgOut.show()
    return (startNode,goalNode)
    
#=============================Main driven=============================
def main():
    img = MyImg(defaultPath)
    img.printInfo()
    start,end,m = readInput("input.txt")
    nodeMat = createNode(img)
    explored = set()
    queue = set()
    startNode, goalNode = run(heuristic2,1)
    startNode.printInfo()
    goalNode.printInfo()

if __name__=="__main__":
    main()