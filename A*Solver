import os
import pygame
import pygame.freetype
import time

#Our Grid of nodes
grid = []

#Grid that helps us determine which spots on the grid are traversable and whichs ones to color appropriately
visualGrid = []

#Finished Path calculated by A*
path = []

"""
Node Class knows its x and y values on the grid, wether or not it is traversable territory, its H and G cost, and its parent node
"""
class Node():
    xPosition = None
    yPosition = None
    walkable = True
    gCost = 0
    hCost = 0
    parent = None
    def __init__(self, _xPosition, _yPosition, _walkable):
        self.xPosition = _xPosition
        self.yPosition = _yPosition
        self.walkable = _walkable

    def setGCost(self, value):
        self.gCost = value

    def setHCost(self, value):
        self.hCost = value

    def setParent(self, value):
        self.parent = value

    def setWalkable(self, value):
        self.walkable = value

    def getFCost(self):
        return (self.gCost + self.hCost)



#Finds Surrounding Nodes

def findSurrounding(node):
    neighbours = []
    for x in range (-1, 2):
        for y in range(-1, 2):
            if (x == 0 and y == 0):
                continue
            checkX = node.xPosition + x
            checkY = node.yPosition + y
            if (checkX >= 0 and checkX < 35 and checkY >= 0 and checkY < 35):
                neighbours.append(grid[checkX][checkY])
    return neighbours

#Gets distance between two nodes
def getDistance(nodeA, nodeB):
    x = abs(nodeA.xPosition - nodeB.xPosition)
    y = abs(nodeA.yPosition - nodeB.yPosition)
    if x > y:
        return 14*y + 10*(x-y)
    return 14*x + 10*(y-x)

#Retraces the finished path of A* and assigns it to the 2d list named path
def retrace(start, end):
    retracedPath = []
    currentNode = end
    while (not currentNode == start):
        retracedPath.append(currentNode)
        currentNode = currentNode.parent
        visualGrid[currentNode.xPosition][currentNode.yPosition] = 3
    retracedPath.reverse()
    path = retracedPath

#Draws Grid Lines
def drawLines():
    for i in range (1, 35):
        pygame.draw.line(screen, (0,0,0), (0,  40 + i * 20), (660, i* 20 + 40), 1)
        pygame.draw.line(screen, (0,0,0), (i * 20, 60), (i* 20, 700), 1)

#setup pygame, the screen and its size.
def setUp():
    global screen
    global run
    global selected
    selected = False
    run = True
    screen = pygame.display.set_mode((660,700))
    screen.fill((255,255,255))
    pygame.display.set_caption("A* Visualizer")

#PyGame initializations:
pygame.font.init()
pygame.freetype.init()
myfont = pygame.freetype.Font("TNR.ttf", 20)
run = True

#Fills Grid with nodes
def setUpGrid():
    new = []
    for i in range (0, 35):
        for j in range (0, 35):
            new.append(0)
        grid.append(new)
        new = []
    for i in range (0, 35):
        for j in range (0, 35):
            grid[i][j] = Node(i , j, True)


#fills visual grid with traversable terrain (0)
def setUpVisualGrid():
    new = []
    for i in range (0, 35):
        for j in range (0, 35):
            new.append(0)
        visualGrid.append(new)
        new = []
    visualGrid[0][0] = 6
    visualGrid[30][30] = 7

#Colors screen in according to visualGrid values
def colorGrid():
    for i in range (0, 35):
        for j in range (0, 35):
            if (visualGrid[i][j] == 1): #Obstacle
                rect = pygame.Rect(i * 20, j * 20 + 60, 20, 20)
                screen.fill((0,0,0), rect)
            if (visualGrid[i][j] == 3): #Path
                rect = pygame.Rect(i * 20, j * 20 + 60, 20, 20)
                screen.fill((0,0, 255), rect)
            if (visualGrid[i][j] == 4): #Closed Set
                rect = pygame.Rect(i * 20, j * 20 + 60, 20, 20)
                screen.fill((255,0, 0), rect)
            if (visualGrid[i][j] == 5): #Open Set
                rect = pygame.Rect(i * 20, j * 20 + 60, 20, 20)
                screen.fill((0,255, 0), rect)
            if (visualGrid[i][j] == 6): #Purple for startNode
                rect = pygame.Rect(i * 20, j * 20 + 60, 20, 20)
                screen.fill((255, 255, 0), rect)
            if (visualGrid[i][j] == 7): #Yellow for targetNode
                rect = pygame.Rect(i * 20, j * 20 + 60, 20, 20)
                screen.fill((255, 0, 255), rect)
    rect = pygame.Rect(80, 20, 20, 20)
    screen.fill((255, 255, 0), rect)
    rect = pygame.Rect(280, 20, 20, 20)
    screen.fill((255, 0, 255), rect)

#Draws Text
def drawText():
    myfont.render_to(screen, (105, 23), "Start Node", (0, 0, 0))
    myfont.render_to(screen, (305, 23), "Target Node", (0, 0, 0))

#Updates which grid spots are walkable
def gridWalkableUpdate():
    for i in range (0, 35):
        for j in range (0, 35):
            if (visualGrid[i][j] == 1):
                grid[i][j].setWalkable(False)

#Deletes the start node
def deleteLastStart():
    for i in range (0, 35):
        for j in range (0, 35):
            if (visualGrid[i][j] == 6):
                visualGrid[i][j] = 0
#Deletes the target node
def deleteLastTarget():
    for i in range (0, 35):
        for j in range (0, 35):
            if (visualGrid[i][j] == 7):
                visualGrid[i][j] = 0

#A*:
def findPath():
    global startNode
    global targetNode
    openSet = []
    closedSet = []
    openSet.append(startNode)
    while (len(openSet) > 0):
        time.sleep(.00001)
        node = openSet[0]
        for i in range (1, len(openSet)):
            if (openSet[i].getFCost() < node.getFCost() or openSet[i].getFCost() == node.getFCost()):
                if (openSet[i].hCost < node.hCost):
                    node = openSet[i]

        openSet.remove(node)
        closedSet.append(node)
        visualGrid[node.xPosition][node.yPosition] = 4 #Red

        if (node.xPosition == targetNode.xPosition and node.yPosition == targetNode.yPosition):
            retrace(startNode,node)
            return

        for neighbour in findSurrounding(node):
            if ((not neighbour.walkable) or neighbour in closedSet):
                continue

            newCostToNeighbour = node.gCost + getDistance(node, neighbour)

            if (newCostToNeighbour < neighbour.gCost or not neighbour in openSet):
                neighbour.setGCost(newCostToNeighbour)
                neighbour.setHCost(getDistance(neighbour, targetNode))
                neighbour.setParent(node)
            if (not neighbour in openSet):
                openSet.append(neighbour)
                visualGrid[neighbour.xPosition][neighbour.yPosition] = 5 #Green

        pygame.display.update()
        screen.fill((255, 255, 255))
        drawLines()
        colorGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

setUp()
setUpGrid()
setUpVisualGrid()
nextClickStart = False
nextClickTarget = False
skipNextClickObst = False
startNode = Node(0, 0, True)
targetNode = Node(30, 30, True)
while run:
    pygame.display.update()
    screen.fill((255, 255, 255))
    drawLines()
    colorGrid()
    drawText()
    if pygame.mouse.get_pressed()[0]:
        if (nextClickStart):
            deleteLastStart()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            visualGrid[int(mouse_x/20)][int(mouse_y/20 - 3)] = 6
            startNode = Node(int(mouse_x/20), int(mouse_y/20 - 3), True)
            nextClickStart = False
            skipNextClickObst = True
        elif (nextClickTarget):
            deleteLastTarget()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            visualGrid[int(mouse_x/20)][int(mouse_y/20 - 3)] = 7
            targetNode = Node(int(mouse_x/20), int(mouse_y/20 - 3), True)
            nextClickTarget = False
            skipNextClickObst = True
        elif (not skipNextClickObst):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            visualGrid[int(mouse_x/20)][int(mouse_y/20 - 3)] = 1
            gridWalkableUpdate()
        #If startnode button clicked
        if (mouse_x > 80 and mouse_x < 100 and mouse_y > 20 and mouse_y < 40):
            nextClickStart = True
        #if targetnode button clicked
        if (mouse_x > 280 and mouse_x < 300 and mouse_y > 20 and mouse_y < 40):
            nextClickTarget = True
        skipNextClickObst = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                findPath()
