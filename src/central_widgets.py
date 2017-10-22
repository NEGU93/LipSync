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

        self.rightLayout.addWidget(label)
        self.rightLayout.addWidget(comboBox)
        self.rightLayout.addWidget(run_algorithm_button)

        self.layout.addLayout(self.rightLayout)

    def right_layout_init(self):
        self.canvas = PlotCanvas()
        self.leftLayout.addWidget(self.canvas)
        self.layout.addLayout(self.leftLayout)

    def plot_data(self, data, filename):
        # import pdb; pdb.set_trace()
        self.canvas.plot(data, filename)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data_to_plot, name):
        ax = self.figure.add_subplot(111)
        ax.plot(data_to_plot, 'b-')
        ax.set_title(name)
        self.draw()
