from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap


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
        # import pdb; pdb.set_trace()
        self.pixmap = QPixmap('../images/mouth_types.jpg')
        self.label.setPixmap(self.pixmap)
        self.leftLayout.addWidget(self.label)

        self.button1 = QPushButton("Button 1")
        self.leftLayout.addWidget(self.button1)

        self.layout.addLayout(self.leftLayout)

    def rightLayout_init(self):
        self.leftLayout = QVBoxLayout(self)
        self.button2 = QPushButton("Button 2")
        self.layout.addWidget(self.button2)
        self.layout.addLayout(self.leftLayout)
