import data
import numpy as np

from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QSizePolicy, QAction, QComboBox
from PyQt5.QtGui import QIcon, QPixmap

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.leftLayout = QVBoxLayout(self)
        self.rightLayout = QVBoxLayout(self)
        self.data = data.LipSyncData.get_instance()
        self.right_layout_init()
        self.left_layout_init()

        self.setLayout(self.layout)

    def left_layout_init(self):
        label = QLabel(self)
        pixmap = QPixmap('../images/mouth_types.jpg')
        label.setPixmap(pixmap)

        comboBox = QComboBox(self)
        comboBox.addItem('Algorithm 1')
        comboBox.addItem('Algorithm 2')

        run_algorithm_button = QPushButton('Run Algorithm', self)
        run_algorithm_button.setToolTip('Run the selected phoneme recognition algorithm')
        run_algorithm_button.clicked.connect(self.run_phonema_recognition_algorithm)

        self.rightLayout.addWidget(label)
        self.rightLayout.addWidget(comboBox)
        self.rightLayout.addWidget(run_algorithm_button)

        self.layout.addLayout(self.rightLayout)

    def right_layout_init(self):
        self.canvas = PlotCanvas()
        self.leftLayout.addWidget(self.canvas)
        self.layout.addLayout(self.leftLayout)

    def plot_data(self, filename):
        # import pdb; pdb.set_trace()
        self.canvas.plot(filename)

    def add_vertical_line(self, sec, remove=True):
        self.canvas.draw_line(sec, remove)

    def run_phonema_recognition_algorithm(self):
        self.data.example_dat()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)
        self.data = data.LipSyncData.get_instance()
        self.fs = 0
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, name):
        # import pdb; pdb.set_trace()
        ax = self.fig.add_subplot(111)
        ax.cla()
        signal, self.fs = self.data.get_audio_fs()
        time = np.linspace(0, len(signal) / self.fs, num=len(signal))
        ax.plot(time, signal, 'b-')
        ax.set_title(name)
        ax.set_xlabel('seconds')
        self.draw()
        ax.axvline(x=0, color='r')

    def draw_line(self, sec, remove=True):
        # import pdb; pdb.set_trace()
        ax = self.fig.add_subplot(111)
        if remove:
            ax.lines[1].remove()
        ax.axvline(x=sec, color='r')
        self.draw()
