import sys, random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor

from tetris_shape import Shape, BOARD_DATA

class Board(QFrame):
    # msg2Statusbar = pyqtSignal(str)
    speed = 1000

    def __init__(self, parent, gridSize):
        super().__init__(parent)
        self.setFixedSize(gridSize * BOARD_DATA.width, gridSize * BOARD_DATA.height)
        self.gridSize = gridSize
        self.initBoard()

    def initBoard(self):
        print('Board initiated')
        self.score = 0
        BOARD_DATA.clear()
    
    def paintEvent(self, event):
        print('printEvent triggered')
        painter = QPainter(self)
        # painter.begin()

        # draw backboard
        for x in range(BOARD_DATA.width):
            for y in range (BOARD_DATA.height):
                val = BOARD_DATA.getValue(x, y)
                drawSquare(painter, x * self.gridSize, y * self.gridSize, val, self.gridSize)
        # draw current shape
        for x, y in BOARD_DATA.getCurShapeCoord():
            val = BOARD_DATA.curShape.shape
            drawSquare(painter, x * self.gridSize, y * self.gridSize, val, self.gridSize)

        # draw the border
        painter.setPen(QColor(0x777777))
        painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height())
        painter.setPen(QColor(0xcccccc))
        painter.drawLine(self.width(), 0, self.width(), self.height())

        # painter.end()
    
    def updateData(self):
        print('Board updated')
        # self.msg2Statusbar.emit(str(self.
        # 1score))
        self.update()

class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.isStarted = False
        self.isPaused = False
        self.nextMove = None
        self.lastShape = Shape.shapeNone

        self.initUI()
    
    def initUI(self):
        self.gridSize = 22
        self.speed = 500

        self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)

        hbox = QHBoxLayout()
        self.tboard = Board(self, self.gridSize)
        hbox.addWidget = self.tboard

        self.statusbar = self.statusBar()
        # self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.start()

        self.center()
        self.setWindowTitle('Tetris')
        self.show()
        self.setFixedSize(self.tboard.width(), 500 + self.statusbar.height())
    
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2 , (screen.height() - size.height()) // 2)
    
    def start(self):
        self.isStarted = True
        self.tboard.score = 0
        BOARD_DATA.clear()

        # self.tboard.msg2Statusbar.emit(str(self.tboard.score))

        BOARD_DATA.createNewPiece()
        self.timer.start(self.speed, self)
    
    def updateWindow(self):
        self.tboard.updateData()
        self.update()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.nextMove:
                k = 0
                while BOARD_DATA.curDirection != self.nextMove[0] and k < 4:
                    BOARD_DATA.rotateRight()
                    k += 1
                k = 0
                while BOARD_DATA.curX != self.nextMove[1] and k < 5:
                    if BOARD_DATA.curX > self.nextMove[1]:
                        BOARD_DATA.moveLeft()
                    elif BOARD_DATA.curX < self.nextMove[1]:
                        BOARD_DATA.moveRight()
                    k += 1
            lines = BOARD_DATA.moveDown()
            self.tboard.score += lines
            if self.lastShape != BOARD_DATA.curShape:
                self.nextMove = None
                self.lastShape = BOARD_DATA.curShape
            self.updateWindow()
        else:
            super(Tetris, self).timerEvent(event)

    def keyPressEvent(self, event):
        if not self.isStarted or BOARD_DATA.curShape == Shape.shapeNone:
            super(Tetris, self).keyPressEvent(event) 
            return
        key = event.key()

        if key == Qt.Key_Left:
            BOARD_DATA.moveLeft()
        elif key == Qt.Key_Right:
            BOARD_DATA.moveRight()
        elif key == Qt.Key_Up:
            BOARD_DATA.rotateLeft()
        elif key == Qt.Key_Down:
            BOARD_DATA.rotateRight()
        else:
            super(Tetris, self).keyPressEvent(event)
        
        self.updateWindow()
    
def drawSquare(painter, x, y, val, s):
    colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                  0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00, 0xFFFFFF]
    if val == 0:
        return
        
    color = QColor(colorTable[val])
    painter.fillRect(x + 1, y + 1, s - 2, s - 2, color)

    painter.setPen(color.lighter())
    painter.drawLine(x, y + s - 1, x, y)
    painter.drawLine(x, y, x + s - 1, y)

    painter.setPen(color.darker())
    painter.drawLine(x + 1, y + s - 1, x + s - 1, y + s - 1)
    painter.drawLine(x + s - 1, y + s - 1, x + s - 1, y + 1)


if __name__ == '__main__':
    # random.seed(32)
    app = QApplication([])
    tetris = Tetris()
    sys.exit(app.exec_())