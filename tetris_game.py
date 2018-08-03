import sys, random
from PyQt5.QtWidgets import QFrame, QMainWindow, QApplication, QDesktopWidget
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal

class Tetris(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        