from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QVBoxLayout


class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.rightLayout_init()
        self.leftLayout_init()

        self.setLayout(self.layout)

    def rightLayout_init(self):
        self.rightLayout = QVBoxLayout(self)
        self.button1 = QPushButton("Button 1")
        self.rightLayout.addWidget(self.button1)
        self.layout.addLayout(self.rightLayout)

    def leftLayout_init(self):
        self.leftLayout = QVBoxLayout(self)
        self.button2 = QPushButton("Button 2")
        self.layout.addWidget(self.button2)
        self.layout.addLayout(self.leftLayout)
