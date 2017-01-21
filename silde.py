from math import sqrt
from sets import Set
from collections import deque

#parse the stdin and change this value as such
SIDE = 0
visited = set()

class node():
    def __init__(self, value):
        self.parent = None
        self.data = value
        self.boardArr = None
        #4 is the max branching factor
        self.availPos = [None] * 4
        self.parent = None
        self.to2D()

    def __repr__(self):
        return self.data

    def printNodes(self):
        for node in self.availPos:
            if(node != None):
                print node.data

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

    def addPos(self, node):
        count = 0
        for pos in self.availPos:
            if(pos == None):
                self.availPos[count] = node
                self.availPos[count].parent = self
                break
            if(pos == None and count == 4):
                print "too much"
            count += 1

    def nextMove(self):
        blankIndex = self.data.index(' ')
        blankCol = blankIndex // SIDE
        blankRow = blankIndex % SIDE
        if (blankCol - 1 >= 0):
            newNode = node(self.swapSpace(self.boardArr[blankRow][blankCol - 1]))
            if (newNode.data not in visited):
                self.addPos(newNode)
                visited.add(newNode.data)
        if (blankCol + 1 < SIDE):
            newNode = node(self.swapSpace(self.boardArr[blankRow][blankCol + 1]))
            if (newNode.data not in visited):
                self.addPos(newNode)
                visited.add(newNode.data)
        if (blankRow - 1 >= 0):
            newNode = node(self.swapSpace(self.boardArr[blankRow - 1][blankCol]))
            if (newNode.data not in visited):
                self.addPos(newNode)
                visited.add(newNode.data)
        if (blankRow + 1 < SIDE):
            newNode = node(self.swapSpace(self.boardArr[blankRow + 1][blankCol]))
            if (newNode.data not in visited):
                self.addPos(newNode)
                visited.add(newNode.data)
        # self.printNodes()

    def swapSpace(self, numberToSwap):
        blankIndex = self.data.index(' ')
        numbIndex = self.data.index(str(numberToSwap))
        newData = list(self.data)
        newData[blankIndex], newData[numbIndex] = newData[numbIndex], newData[blankIndex]
        newData = "".join(newData)
        return newData

class tree():
    def __init__(self, root):
        self.root = root
        self.visited = {root.data}

    def BFS(self):
        queue = deque([self.root])
        while (len(queue) > 0):
            currNode = queue.popleft()
            # if (currNode.data == '123456789abcdef '):
            if (currNode.data == '12345678 '):
                break
            currNode.nextMove()
            for node in currNode.availPos:
                if (node != None):
                    queue.append(node)

        while (currNode != None):
            print currNode
            currNode = currNode.parent

    def DFS(self):
        stack = deque([self.root])
        while (len(stack) > 0):
            currNode = stack.pop()
            # if (currNode.data == '123456789abcdef '):
            if (currNode.data == '12345678 '):
                break
            currNode.nextMove()
            for node in currNode.availPos:
                if (node != None):
                    stack.append(node)

        while (currNode != None):
            print currNode
            currNode = currNode.parent


# node0 = node("abc123456789def ")
node0 = node('1234 5678')
tree0 = tree(node0)

# tree0.BFS()
tree0.DFS()
