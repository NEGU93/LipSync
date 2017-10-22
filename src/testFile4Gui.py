import sys
from PyQt4 import QtGui, QtCore


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")

        extractAction = QtGui.QAction("&GET TO THE CHOPPAH!!!", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

        self.home()

    def home(self):
        btn = QtGui.QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.minimumSizeHint())
        btn.move(0, 100)

        extractAction = QtGui.QAction(QtGui.QIcon('todachoppa.png'), 'Flee the Scene', self)
        extractAction.triggered.connect(self.close_application)

        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction)

        self.show()

    def close_application(self):
        print("whooaaaa so custom!!!")
        sys.exit()


def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()