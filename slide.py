import sys
from math import sqrt
from sets import Set
from collections import deque
from heapq import heappush, heappop

#parse stuff - its messy, oh well it works
COMPLETED = None
COMPLETEDALT = '123456789abcdfe '
heuristicToUse = None

messed = sys.argv[1]
command = sys.argv[2]
if (len(sys.argv) > 3):
    heuristicToUse = sys.argv[3]

if(len(messed) == 9):
    COMPLETED = '12345678 '
if(len(messed) == 16):
    COMPLETED = '123456789abcdef '

SIDE = 0
visited = set()

class node():
    #creates a node, or a board state
    def __init__(self, value):
        self.parent = None
        self.data = value
        self.boardArr = None
        #4 is the max branching factor
        self.availPos = [None] * 4
        self.parent = None
        self.to2D()
        self.level = 0
        self.estiH = 0

    #prints the board that the node represents
    def __repr__(self):
        return self.data

    #Prints the nodes (or possible board states) of the current node
    def printNodes(self):
        for node in self.availPos:
            if(node != None):
                print node.data

    #Resource heavy method that turns the 1D represntation of the board
    #into its 2D equivalent
    def to2D(self):
        global SIDE
        length = len(self.data)
        SIDE = int(sqrt(length))
        self.boardArr = [[0 for x in range(SIDE)] for y in range(SIDE)]
        x = 0
        y = 0
        for letter in self.data:
            letterAdd = None
            if(letter != ' '):
                letterAdd = letter
            else:
                letterAdd = 0
            self.boardArr[x][y] = letterAdd
            if x < SIDE - 1:
                x += 1
            else:
                y += 1
                x = 0

    #Adds a new node (or board state) to the current node.
    #Can pass in a heursitic to set an cost estimation
    def addPos(self, node, heuristic = None):
        count = 0
        for pos in self.availPos:
            if(pos == None):
                self.availPos[count] = node
                self.availPos[count].parent = self
                self.availPos[count].level = self.level + 1
                if(heuristic != None):
                    self.availPos[count].estiH = heuristic(self.availPos[count].data)
                break
            if(pos == None and count == 4):
                print "too much"
            count += 1

    #finds the (max 4) moves that can be done
    def nextMove(self, heuristic = None):
        nodesCreated = 0
        blankIndex = self.data.index(' ')
        blankCol = blankIndex // SIDE
        blankRow = blankIndex % SIDE
        if (blankCol - 1 >= 0):
            newNode = node(self.swapSpace(self.boardArr[blankRow][blankCol - 1]))
            if (newNode.data not in visited):
                nodesCreated += 1
                self.addPos(newNode, heuristic)
                visited.add(newNode.data)
        if (blankCol + 1 < SIDE):
            newNode = node(self.swapSpace(self.boardArr[blankRow][blankCol + 1]))
            if (newNode.data not in visited):
                nodesCreated += 1
                self.addPos(newNode, heuristic)
                visited.add(newNode.data)
        if (blankRow - 1 >= 0):
            newNode = node(self.swapSpace(self.boardArr[blankRow - 1][blankCol]))
            if (newNode.data not in visited):
                nodesCreated += 1
                self.addPos(newNode, heuristic)
                visited.add(newNode.data)
        if (blankRow + 1 < SIDE):
            newNode = node(self.swapSpace(self.boardArr[blankRow + 1][blankCol]))
            if (newNode.data not in visited):
                nodesCreated += 1
                self.addPos(newNode, heuristic)
                visited.add(newNode.data)
        return nodesCreated

    #Swaps the tiles values to emulate sliding
    def swapSpace(self, numberToSwap):
        blankIndex = self.data.index(' ')
        numbIndex = self.data.index(str(numberToSwap))
        newData = list(self.data)
        newData[blankIndex], newData[numbIndex] = newData[numbIndex], newData[blankIndex]
        newData = "".join(newData)
        return newData

class tree():
    #creates a tree that has the search strategies
    def __init__(self, root):
        self.root = root
        self.visited = {root.data}

    #Breadth first search
    def BFS(self, startNode):
        queue = deque([startNode])
        nodesCreated = 0
        nodesExpanded = 0
        while (len(queue) > 0):
            currNode = queue.popleft()
            nodesExpanded += 1
            if (currNode.data == COMPLETED or currNode.data == COMPLETEDALT):
                break
            nodesCreated += currNode.nextMove()
            for node in currNode.availPos:
                if (node != None):
                    queue.append(node)

        print(currNode.level, nodesCreated, nodesExpanded, len(queue))
        # while (currNode != None):
        #     print currNode
        #     currNode = currNode.parent

    #Depth first search
    def DFS(self, startNode):
        stack = deque([startNode])
        nodesCreated = 0
        nodesExpanded = 0
        while (len(stack) > 0):
            currNode = stack.pop()
            nodesExpanded += 1
            if (currNode.data == COMPLETED or currNode.data == COMPLETEDALT):
                break
            nodesCreated += currNode.nextMove()
            for node in currNode.availPos:
                if (node != None):
                    stack.append(node)

        print(currNode.level, nodesCreated, nodesExpanded, len(stack))
        # while (currNode != None):
        #     print currNode
        #     currNode = currNode.parent

    #Searchs for a solution until the set tree level
    #returns -1 if solution is not found
    def DLS(self, startNode, limit, silent):
        nodesCreated = 0
        nodesExpanded = 0
        found = False
        stack = deque([startNode])
        while (len(stack) > 0):
            currNode = stack.pop()
            nodesExpanded += 1
            if (currNode.data == COMPLETED or currNode.data == COMPLETEDALT):
                found = True
                break
            nodesCreated += currNode.nextMove()
            for node in currNode.availPos:
                if (node != None and node.level < limit):
                    stack.append(node)

        if(found == True):
            print(currNode.level, nodesCreated, nodesExpanded, len(stack))
            # while (currNode != None):
            #     print currNode
            #     currNode = currNode.parent
        else:
            if (silent == False):
                print "No solution"
            return -1

    #continously increases depth of the search until a solution is found
    def IDS(self, startNode):
        limit = 0
        found = -1
        while(found == -1):
            limit += 1
            found = self.DLS(startNode, limit, True)

        print "answer found at:", limit

    #Chooses the next node that has the smallest heurstic value. Uses heapsort/
    #prioity queue to determine this
    def greedy(self, startNode, heuristic):
        nodesCreated = 0
        nodesExpanded = 0
        prioQueue = [(0, startNode)]
        while(len(prioQueue) > 0):
            currNode = heappop(prioQueue)[1]
            nodesExpanded += 1
            if (currNode.data == COMPLETED or currNode.data == COMPLETEDALT):
                break
            nodesCreated += currNode.nextMove(heuristic)
            for node in currNode.availPos:
                if (node != None):
                    heappush(prioQueue, (node.estiH, node))

        print(currNode.level, nodesCreated, nodesExpanded, len(prioQueue))
        # while(currNode != None):
        #     print currNode
        #     currNode = currNode.parent

#Heuristic that finds the distance tiles are away from their correct position
#Returns a sum of the distances
def distH(boardData):
    global SIDE
    estimation = 0
    for tile in boardData:
        if (tile != ' '):
            #integer distance formula - Made it up, does it exist already?
            boardIndex = boardData.index(tile)
            boardCol = boardIndex // SIDE
            boardRow = boardIndex % SIDE

            compIndex = COMPLETED.index(tile)
            compCol = compIndex // SIDE
            compRow = compIndex % SIDE
            estimation += abs(boardCol - compCol) + abs(boardRow - compRow)

    return estimation

#Heuristic that finds how many tiles that are not in the correct position
#returns the number of tiles that are not in the correct posistion
def locaH(boardData):
    value = 0
    for tile in boardData:
        if (COMPLETED.index(tile) != boardData.index(tile)):
            value += 1
    return value

#A* heurstic is just the sum of the previous two hueristics
def aStarH(boardData):
    return locaH(boardData) + distH(boardData)

node0 = node(messed)
tree = tree(node0)

if(command.lower() == 'bfs'):
    tree.BFS(node0)
if(command.lower() == 'dfs'):
    tree.DFS(node0)
if(command.lower() == 'ids'):
    tree.IDS(node0)
if(command.lower() == 'gbfs'):
    if(heuristicToUse.lower() == 'h1'):
        tree.greedy(node0, locaH)
    if(heuristicToUse.lower() == 'h2'):
        tree.greedy(node0, distH)
if(command.lower() == 'astar'):
    tree.greedy(node0, aStarH)
if(command.lower() == 'test'):
    node0.nextMove()
    print node0.availPos
