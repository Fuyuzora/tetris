import random


class Block(object):
    blockNone = 0
    blockI = 1
    blockL = 2
    blockJ = 3
    blockS = 4
    blockZ = 5
    blockT = 6
    blockO = 7

    blockCoords = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, 2), (0, 1), (0, 0), (0, -1)),
        ((0, 1), (0, 0), (0, -1), (1, -1)),
        ((1, 1), (1, 0), (1, -1), (0, -1)),
        ((0, 1), (0, 0), (1, 0), (1, -1)),
        ((1, 1), (1, 0), (0, 0), (0, -1)),
        ((0, 1), (0, 0), (0, -1), (1, 0)),
        ((0, 0), (1, 0), (0, -1), (1, -1))
    )

    def __init__(self, block=0):
        self.block = block
        self.currentCoords = self.blockCoords(block)

    def rotatesRight(self, test):
        if not test:
            self.currentCoords = ((-y, x) for (x, y) in self.currentCoords)
        else:
            return ((-y, x) for (x, y) in self.currentCoords)

    def rotatesLeft(self, test):
        if not test:
            self.currentCoords = ((y, -x) for (x, y) in self.currentCoords)
        else:
            return ((y, -x) for (x, y) in self.currentCoords)

    def getCurrentCoords(self):
        return ((x, y) for (x, y) in self.currentCoords)


class GameData(object):
    boardWidth = 20
    boardHeight = 35
    boardSize = 700

    def __init__(self):
        self.currentX = -1
        self.currentY = -1
        self.currentBlock = Block()
        self.nextBlock = Block(random.randint(1, 7))
        self.boardInfo = [0] * GameData.boardWidth * GameData.boardHeight

    def getCurrentBlock(self):
        return self.currentBlock

    def tryMoveDown(self):
        for (x, y) in self.currentBlock.getCurrentCoords():
            if self.boardInfo[x + self.currentX][y - 1 + self.currentY] != True:
                return False
        return True

    def tryRotateLeft(self):
        tmpCoords = self.currentBlock.rotatesLeft(True)
        for (x, y) in tmpCoords:
            if self.boardInfo[x + self.currentX][y + self.currentY] != True:
                return False
        return True

    def tryRotateRight(self):
        tmpCoords = self.currentBlock.rotatesRight(True)
        for (x, y) in tmpCoords:
            if self.boardInfo[x + self.currentX][y + self.currentY] != True:
                return False
        return True

    # -1 for left adn 1 for right
    def tryMoveSideways(self, direction):
        tmpCoords = self.currentBlock.getCurrentCoords()
        for (x, y) in tmpCoords:
            if self.boardInfo[x + direction + self.currentX][y + self.currentY] != True:
                return False
        return True

    def moveDown(self):
        if self.tryMoveDown():
            self.currentY -= 1
        else:
            self.merge()

    def rotateRight(self):
        if self.tryRotateRight():
            self.currentBlock.rotatesRight(False)

    def rotateLeft(self):
        if self.tryRotateLeft():
            self.currentBlock.rotatesLeft(False)

    def moveSideways(self, direction):
        if self.tryMoveSideways(direction):
            self.currentX += direction

    def newBlock(self):
        if (self.tryMoveDown):
            self.currentBlock = Block()
        else:
            self.currentBlock = self.nextBlock()

    def merge(self):
        for (x, y) in self.currentBlock.getCurrentCoords():
            self.boardInfo[x][y] = True
        self.clearFilledRow()
        self.currentBlock = self.nextBlock

    def clearFilledRow(self):
        completed = 0
        for row in (0, 25):
            rowNum = row
            for col in (0, 10):
                if self.boardInfo[row][col] != True:
                    break
                elif col == 9:
                    completed += 1
                    for colNum in (0, 10):
                        self.boardInfo[row][colNum] = False
        if completed > 0:
            for x in (rowNum, 25):
                for y in (0, 10):
                    if self.boardInfo[x][y] == True:
                        self.boardInfo[x][y] = False
                        self.boardInfo[x][y - completed] = True
