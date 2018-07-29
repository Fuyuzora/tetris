from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QHBoxLayout
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor

import sys
import random

from tetris_blocks import Block, GameData


class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.started = False
        self.nextMove = False
        self.lastBlock = Block.blockNone

        self.initUI()

    def initUI(self):
        self.gridSize = 20
        self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)

        hbox = QHBoxLayout()
        self.tboard = Board(self, self.gridSize)
        hbox.addLayout(self.tboard)

        self.start()

        self.setWindowTitle('Tetris')
        self.show()
        self.setFixedSize(self.tboard.width(), 300)

    def start(self):
        self.started = True
        self.tboard.score = 0

        GameData.newBlock()

        self.timer.start()

    def updateWindow(self):
        self.tboard.updateData()
        self.update()

    def keyPressEvent(self, event):
        if not self.isStarted or GameData.currentBlock == Block.blockNone:
            super(Tetris, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return
        elif key == Qt.Key_Left:
            GameData.moveSideways(-1)
        elif key == Qt.Key_Right:
            GameData.moveSideways(1)
        else:
            super(Tetris, self).keyPressEvent(event)

        self.updateWindow()


class Board(QFrame):

    def __init__(self, parent, gridSize):
        super().__init__(parent)
        self.setFixedSize(gridSize * GameData.boardWidth,
                          gridSize * GameData.boardHeight)
        self.gridSize = gridSize
        self.initBoard()

    def initBoard(self):
        self.score = 0

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw backboard
        for x in range(GameData.boardWidth):
            for y in range(GameData.boardHeight):
                val = GameData.getBoardInfo[x, y]
                drawSquare(painter, x * self.gridSize, y *
                           self.gridSize, val, self.gridSize)

        # Draw current shape
        for x, y in GameData.:
            val = GameData.currentShape.shape
            drawSquare(painter, x * self.gridSize, y *
                       self.gridSize, val, self.gridSize)

        # Draw a border
        painter.setPen(QColor(0x777777))
        painter.drawLine(self.width()-1, 0, self.width()-1, self.height())
        painter.setPen(QColor(0xCCCCCC))
        painter.drawLine(self.width(), 0, self.width(), self.height())


def drawSquare(painter, x, y, val, s):
    colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

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
