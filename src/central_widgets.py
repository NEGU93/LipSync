from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QSizePolicy, QAction
from PyQt5.QtGui import QIcon, QPixmap

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.rightLayout_init()
        self.leftLayout_init()

        self.setLayout(self.layout)

    def leftLayout_init(self):
        self.leftLayout = QVBoxLayout(self)

        self.label = QLabel(self)
        self.pixmap = QPixmap('../images/mouth_types.jpg')
        self.label.setPixmap(self.pixmap)
        self.leftLayout.addWidget(self.label)

        self.layout.addLayout(self.leftLayout)

    def rightLayout_init(self):
        self.leftLayout = QVBoxLayout(self)
        self.canvas = PlotCanvas()
        self.leftLayout.addWidget(self.canvas)
        self.button2 = QPushButton("Button 2")
        self.leftLayout.addWidget(self.button2)
        self.layout.addLayout(self.leftLayout)

    def plotData(self, data, filename):
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
