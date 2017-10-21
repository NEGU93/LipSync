import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class LipSyncData():
    def __init__(self):
        self.audio = []

    def open_wav(self, path):
        print('Open wav file with this path:' + path)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'LipSync - by Matias Dwek & Agustin Barrachina'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.data = LipSyncData()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.addMenu()

        self.show()

    def addMenu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        # Under File
        # Open File
        openButton = QAction('Open', self)
        openButton.setShortcut("Ctrl+E")
        openButton.setStatusTip("Open wav file")
        openButton.triggered.connect(self.open)
        fileMenu.addAction(openButton)
        # Export file
        exportButton = QAction('Export', self)
        fileMenu.addAction(exportButton)
        # Exit Button
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

    def open(self):
        print('open file')
        path = 'hola'
        self.data.open_wav(path=path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
