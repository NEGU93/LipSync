import sys
import wave
import struct
import central_widgets
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QAction, QFileDialog, QGroupBox, QHBoxLayout, \
    QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class LipSyncData():
    def __init__(self):
        self.audio = []

    def open_wav(self, path):
        sound_frames, fs = self.wav_to_floats(path)
        self.audio = np.asarray(sound_frames)

    def wav_to_floats(self, path):
        w = wave.open(path)
        fs = w.getframerate()
        astr = w.readframes(w.getnframes())
        # convert binary chunks to short
        a = struct.unpack("%ih" % (w.getnframes() * w.getnchannels()), astr)
        a = [float(val) / pow(2, 15) for val in a]
        return a, fs


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

        self.form_widget = central_widgets.FormWidget(self)
        self.setCentralWidget(self.form_widget)

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
        openButton.setShortcut("Ctrl+O")
        openButton.setStatusTip("Open wav file")
        openButton.triggered.connect(self.file_open)
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

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open File', filter='*.wav')
        print('Path: ' + path)
        self.data.open_wav(path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
