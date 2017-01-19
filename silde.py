import math

class node():
    def __init__(self, value):
        self.data = value
        self.dataArr = self.to2D(value)
        self.availPos = [None] * 4
        self.parent = None

    def printNodes(self):
        for node in self.availPos:
            if(node != None):
                print node.data

    def to2D(self, board):
        length = len(board)
        side = int(math.sqrt(length))
        self.dataArr = [[0 for x in range(side)] for y in range(side)]
        x = 0
        y = 0
        for letter in board:
            self.dataArr[x][y] = letter
            if x < side - 1:
                x += 1
            else:
                y += 1
                x = 0

class tree():
    def __init__(self, root):
        self.root = root
        self.visited = {root.data}

    def add(self, node):
        count = 0
        for pos in self.root.availPos:
            if(pos == None):
                self.root.availPos[count] = node
                break
            count += 1

    #def BFS(self, node):

node0 = node("12345678 ")
print node0.dataArr
