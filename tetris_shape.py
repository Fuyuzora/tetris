import random


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
        return (minx, maxx, minY, maxY)

class BoardData(object):
    width = 10
    height = 22

    def __init__(self):
        self.backBoard = [0] * BoardData.width * BoardData.height

        self.curX = -1
        self.curY = -1
        self.curDirection = 0
        self.curShape = Shape()
        self.nextShape = Shape(random.randint(1, 7))

    def getData(self):
        return self.backBoard[:]
    
    def getValue(self, x, y):
        return self.backBoard[x + y * BoardData.width]