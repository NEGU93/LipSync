from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, databaseFilePath, userFilePath):
        super(MainWindow, self).__init__()
        self.databaseFilePath = databaseFilePath
        self.userFilePath = userFilePath
        self.createUI()

    def changeFilePath(self):
        print('changeFilePath')

    def createUI(self):
        self.setWindowTitle('Equipment Manager 0.3')
        menu = self.menuBar().addMenu('File')
        action = menu.addAction('Open')
        action.triggered.connect(self.changeFilePath)

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow('some/path', 'some/other/path')
    window.show()
    window.setGeometry(500, 300, 300, 300)
    sys.exit(app.exec_())

