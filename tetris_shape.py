import random, math


class Shape(object):
    shapeNone = 0
    shapeI = 1
    shapeL = 2
    shapeJ = 3
    shapeT = 4
    shapeO = 5
    shapeS = 6
    shapeZ = 7

    shapeCoord = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((0, -1), (0, 0), (0, 1), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (-1, 1)),
        ((0, -1), (0, 0), (0, 1), (1, 0)),
        ((0, 0), (0, -1), (1, 0), (1, -1)),
        ((0, 0), (0, -1), (-1, 0), (1, -1)),
        ((0, 0), (0, -1), (1, 0), (-1, -1))
    )

    def __init__(self, shape=0):
        self.shape = shape

    def getRotatedOffsets(self, direction):
        tmpCoords = Shape.shapeCoord[self.shape]
        # no direction change
        if direction == 0 or self.shape == Shape.shapeO:
            return ((x, y) for x, y in tmpCoords)
        # 90 cw
        if direction == 1:
            return ((-y, x) for x, y in tmpCoords)

        # 180 cw/ccw
        if direction == 2:
            if self.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
                return ((x, y) for x, y in tmpCoords)
            else:
                return ((-x, -y) for x, y in tmpCoords)
        # 90 ccw
        if direction == 3:
            if self.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
                return ((-y, x) for x, y in tmpCoords)
            else:
                return ((y, -x) for x, y in tmpCoords)

    def getCoords(self, direction, offX, offY):
        return ((x + offX, y + offY) for x, y in self.getRotatedOffsets(direction))

    def getBoundingOffsets(self, direction):
        tmpCoords = self.getRotatedOffsets(direction)
        minX, maxX, minY, maxY = 0, 0, 0, 0
        for x, y in tmpCoords:
            if minX > x:
                minX = x
            if maxX < x:
                maxX = x
            if minY > y:
                minY = y
            if maxY > y:
                maxY = y
        return (minX, maxX, minY, maxY)

class BoardData(object):
    width = 16
    height = 22

    def __init__(self):
        self.backBoard = [0] * BoardData.width * BoardData.height

        self.curX = -1
        self.curY = -1
        self.curDirection = 0
        self.curShape = Shape()
        self.nextShape = Shape(random.randint(1, 7))

        self.shapeStatus = [0] * 8

    def getData(self):
        return self.backBoard[:]
    
    def getValue(self, x, y):
        return self.backBoard[x + y * BoardData.width]
    
    def getCurShapeCoord(self):
        return self.curShape.getCoords(self.curDirection, self.curX, self.curY)
    
    def getCurrentDirection(self):
        return self.curDirection
    
    def getWidth(self):
        return self.width
    
    def tryMove(self, shape, direction, x, y):
        for x, y in shape.getCoords(direction, x, y):
            if x >= BoardData.width:
                # print('hit right boundary')
                return False
            elif x < 0:
                # print('hit left boundary')
                return False
            elif y < 0:
                # print('hit upper boundary')
                return False
            elif y >= BoardData.height:
                # print('hit lower boundary, current y = '+str(y))
                return False
            # if x >= BoardData.width or x < 0 or y < 0 or y >= BoardData.height:
            #     print('hit boundary')
                # return False
            if self.backBoard[int(x + y * BoardData.width)] > 0:
                # print('hit other blocks at row:'+str(y)+'col: '+str(x))
                return False
        return True
    
    def tryMoveCurrent(self, direction, x, y):
        return self.tryMove(self.curShape, direction, x, y)
    
    def createNewPiece(self):
        minX, maxX, minY, maxY = self.nextShape.getBoundingOffsets(0)
        result = False
        if self.tryMoveCurrent(0, self.width / 2, -minY):
            self.curX = self.width / 2
            self.curY = -minY + 1
            self.curDirection = 0
            self.curShape = self.nextShape
            self.nextShape = Shape(random.randint(1, 7))
            result = True
        else:
            print('you died')
            self.curShape = Shape()
            self.curX = -1
            self.curY = -1
            self.curDirection = 0
            result = False
        self.shapeStatus[self.curShape.shape] += 1
        return result 

    def moveDown(self, ai):
        if self.tryMoveCurrent(self.curDirection, self.curX, self.curY + 1):
            self.curY += 1
            return True
        else:
            self.mergePiece()
            if not ai:
                self.removeFilledLines()
            self.createNewPiece()
            return False
    
    def moveLeft(self):
        if self.tryMoveCurrent(self.curDirection, self.curX - 1, self.curY):
            self.curX -= 1
            return True
        return False
    
    def moveRight(self):
        if self.tryMoveCurrent(self.curDirection, self.curX + 1, self.curY):
            self.curX += 1
            return True
        return False
    
    def rotateRight(self):
        if self.tryMoveCurrent((self.curDirection + 1) % 4, self.curX, self.curY):
            self.curDirection += 1
            self.curDirection %= 4

    def rotateLeft(self):
        if self.tryMoveCurrent((self.curDirection - 1) % 4, self.curX, self.curY):
            self.curDirection -= 1
            self.curDirection %= 4

    def removeFilledLines(self):
        newBackBoard = [0] * BoardData.height * BoardData.width
        newY = BoardData.height - 1
        lines = 0
        for y in range (BoardData.height - 1, -1, -1):
            blockCount = sum([1 if self.backBoard[x + y * BoardData.width] > 0 else 0 for x in range(BoardData.width)])
            if blockCount < BoardData.width:
                for x in range(BoardData.width):
                    newBackBoard[x + newY * BoardData.width] = self.backBoard[x + y * BoardData.width]
                newY -= 1
            else:
                lines += 1
        if lines > 0:
            self.backBoard = newBackBoard
        return lines

    def mergePiece(self):
        for x, y in self.curShape.getCoords(self.curDirection, self.curX, self.curY):
            self.backBoard[int(x + y * BoardData.width)] = self.curShape.shape
        
        self.curX = -1
        self.curY = -1
        self.curDirection = 0
        self.curShape = Shape()
    
    def clear(self):
        self.curX = -1
        self.curY = -1
        self.curDirection = 0
        self.curShape = Shape()
        self.backBoard = [0] * BoardData.width * BoardData.height
    
    def aggregatedHeight(self):
        board = self.getData()
        h = 0
        for c in range(self.width):
            h += self.columnHeight(c)
        return h

    def columnHeight(self, c):
        board = self.getData()
        h = 0
        for r in range(self.height):
            if board[c + r * self.width] != 0:
                h += 1
        return h

    def bumpiness(self):
        total = 0
        for c in range(self.width - 1):
            total += abs(self.columnHeight(c) - self.columnHeight(c+1))
        return total
    
    def holes(self):
        count = 0
        for c in range(self.width):
            block = False
            for r in range(self.height):
                if self.backBoard[c + r * self.width] != 0:
                    block = True
                elif (self.backBoard[c + r * self.width] == 0 and block):
                    count += 1
        return count
    
    def isLine(self, r):
        for c in range(self.width):
            if (self.backBoard[c + r * self.width] == 0):
                return False
        return True

    def lines(self):
        count = 0
        for r in range(self.height):
            if (self.isLine(r)):
                count += 1
        self.removeFilledLines()
        return count

BOARD_DATA = BoardData()