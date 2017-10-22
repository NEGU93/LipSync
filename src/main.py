import sys
import wave
import struct
import central_widgets
import numpy as np

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QAction, QFileDialog, QGroupBox, QHBoxLayout, \
    QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class LipSyncData:
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
        self.form_widget = central_widgets.FormWidget(self)
        self.toolbar = self.addToolBar('Main Toolbar')
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('../images/icons/body_6-512.png'))
        self.add_menu()
        self.add_toolbar()

        self.setCentralWidget(self.form_widget)

        self.show()

    def add_menu(self):
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        edit_menu = main_menu.addMenu('Edit')
        view_menu = main_menu.addMenu('View')
        search_menu = main_menu.addMenu('Search')
        tools_menu = main_menu.addMenu('Tools')
        help_menu = main_menu.addMenu('Help')

        # Under File
        # Open File
        open_button = QAction('Open', self)
        open_button.setShortcut("Ctrl+O")
        open_button.setStatusTip("Open wav file")
        open_button.triggered.connect(self.file_open)
        file_menu.addAction(open_button)
        # Export file
        export_button = QAction('Export', self)
        file_menu.addAction(export_button)
        # Exit Button
        exit_button = QAction(QIcon('exit24.png'), 'Exit', self)
        exit_button.setShortcut('Ctrl+Q')
        exit_button.setStatusTip('Exit application')
        exit_button.triggered.connect(self.close)
        file_menu.addAction(exit_button)

    def add_toolbar(self):
        open_button = QAction(QIcon('../images/icons/149334.svg'), 'Open File', self)
        open_button.triggered.connect(self.file_open)

        export_button = QAction(QIcon('../images/icons/extract.svg'), 'Open File', self)

        play_button = QAction(QIcon('../images/icons/play.svg'), 'Open File', self)

        pause_button = QAction(QIcon('../images/icons/pause.svg'), 'Open File', self)

        stop_button = QAction(QIcon('../images/icons/stop.svg'), 'Open File', self)

        self.toolbar.addAction(open_button)
        self.toolbar.addAction(export_button)
        self.toolbar.addAction(play_button)
        self.toolbar.addAction(pause_button)
        self.toolbar.addAction(stop_button)

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open File', filter='*.wav', directory='../sounds/')
        self.data.open_wav(path)
        filename = path.split('/')
        self.form_widget.plot_data(self.data. audio, filename[len(filename) - 1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
