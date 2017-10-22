import sys
import wave
import struct
import central_widgets
import numpy as np

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QAction, QFileDialog, QGroupBox, QHBoxLayout, \
    QVBoxLayout, QWidget, QSizePolicy
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
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 400
        self.data = LipSyncData()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('../images/icons/body_6-512.png'))
        self.addMenu()
        self.addToolbar()

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

    def addToolbar(self):
        self.toolBar = self.addToolBar('Main Toolbar')

        openButton = QAction(QIcon('../images/icons/149334.svg'), 'Open File', self)
        openButton.triggered.connect(self.file_open)

        exportButton = QAction(QIcon('../images/icons/extract.svg'), 'Open File', self)

        playButton = QAction(QIcon('../images/icons/play.svg'), 'Open File', self)

        pauseButton = QAction(QIcon('../images/icons/pause.svg'), 'Open File', self)

        stopButton = QAction(QIcon('../images/icons/stop.svg'), 'Open File', self)

        self.toolBar.addAction(openButton)
        self.toolBar.addAction(exportButton)
        self.toolBar.addAction(playButton)
        self.toolBar.addAction(pauseButton)
        self.toolBar.addAction(stopButton)

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open File', filter='*.wav', directory='../sounds/')
        self.data.open_wav(path)
        filename = path.split('/')
        self.form_widget.plotData(self.data. audio, filename[len(filename)-1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
