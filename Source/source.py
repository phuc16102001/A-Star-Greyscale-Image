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

#=============================Library========================================
from MyImg import *
from constant import *
from MyMath import *
from MyNode import *

#=============================Heuristic function=============================
#UCS
def heuristic1(pos,goal):
    return 0

#Euclid
def heuristic2(pos,goal):
    return pos.euclidDistance(goal)

#Manhattan
def heuristic3(pos,goal):
    (px,py)=pos.pos()
    (gx,gy)=goal.pos()
    return abs(px-gx)+abs(py-gy)

#Euclid with alpha
def heuristic4(pos,goal):
    return pos.distanceTo(goal)
#=============================File function==================================

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

#Write the cost and number of node it touched to file
#Input: path of file, cost, nTouch
def writeOutput(path,cost,nTouch):
    regex = "%.2f\n%d"
    fout = open(path,'w')
    fout.write(regex%(cost,nTouch))
    fout.close()

#=============================Utils function===================================
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
    height = len(nodeMat)
    width = len(nodeMat[0])

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

#Add a node to the queue
#Input: queue, parent, node, goal, hFunction = set, Node, Node, Node, Pointer to a float-return function
#Description: Add [node] to [queue] whose [parent] and [goal] with the heuristic function [hFunction]
def addNode(queue,parent,node,goal,hFunction):
    if (node in queue):
        oldG = node.g
        newG = parent.g+parent.distanceTo(node)
        if (newG<oldG):
            node.setParent(parent)
    else:
        node.setParent(parent)
        node.setH(hFunction(node,goal))
        queue.add(node)
    
#Draw the image with the list nodes with a specified color
#Input: nodes list, input image, path for new image, color
#Output: the image after draw = MyImg
def drawNode(nodes,img,path,color):
    imgOut = img.copy(path)
    for node in nodes:
        imgOut.write(node.pos(),color)
    imgOut.save()     
    return imgOut           


#Running function
#Input: img, hFunc, startPos, endPos, m = MyImage, Pointer to float-return function, tuples, tuples. int
#Output: path, cost, nTouchNode
def run(img, hFunc, startPos, endPos, m):
    #Explored and queue set
    explored = set()
    queue = set()
    touch = set()

    #Copy into a new image
    nodeMat = createNode(img)
    
    #Get the start and goal node
    startNode = nodeMat[startPos[1]][startPos[0]]
    goalNode = nodeMat[endPos[1]][endPos[0]]
    
    #Add the startNode to queue
    addNode(queue,startNode,startNode,goalNode,hFunc)
    touch.add(startNode)

    #If the queue is not empty
    while (len(queue)>0):
        #Pop the highest priority out (lowest Node.f)
        node = min(queue,key=priority)

        #If we found the goal (end searching)
        if (node==goalNode):
            #Traceback
            result = []
            while (node!=startNode):
                result.append(node)
                node=node.parent
            result.append(startNode)
            result = result[::-1]
            return (result,result[-1].g,touch)
        
        #Not goal
        queue.remove(node)                                              #Remove the poped
        explored.add(node)                                              #Add to explored set
        neighboor = getNeighboor(nodeMat,m,node)                        #Get list of node that can move
        for i in range(len(neighboor)):                                 #For each node
            if not(neighboor[i] in explored):                           #Not in explored      
                addNode(queue,node,neighboor[i],goalNode,hFunc)         #Add that neighboor to queue if it better
                touch.add(neighboor[i])
    return None    

#=============================Main driven=============================
def main():
    #Input
    print("Reading input...")
    img = MyImg(bmpInPath)
    startPos, endPos, m = readInput(inputPath)
    img.printInfo()
    print("Start position:",startPos)
    print("End position: ",endPos)
    print("m:",m)

    #Heuristic function list
    hList = [heuristic1,heuristic2,heuristic3,heuristic4]

    #Each function
    for i in range(len(hList)):             
        print("Running heuristic %d:"%(i+1),end=" ")
        
        #Get the result
        path, cost, touch = run(img, hList[i], startPos, endPos, m)
        nTouch = len(touch)

        #If found path
        if (path!=None):
            print(cost,nTouch)
            drawNode(path, img, bmpOutPath%(i+1), colorRed)         #Draw the output image
            drawNode(touch, img, bmpTouchPath%(i+1), colorBlue)     #Draw the touched image
            writeOutput(outputPath%(i+1), cost, nTouch)             #Write to file

if __name__=="__main__":
    main()