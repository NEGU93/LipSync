import sys
import data
import time
import central_widgets

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QAction, QFileDialog, QGroupBox, QHBoxLayout, \
    QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets


def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None,
                                   "An exception was raised",
                                   "Exception type: {}".format(t))
    old_hook(t, val, tb)


old_hook = sys.excepthook
sys.excepthook = catch_exceptions


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'LipSync - by Matias Dwek & Agustin Barrachina'
        self.left = 100
        self.top = 100
        self.width = 1200
        self.height = 400
        self.data = data.LipSyncData.get_instance()
        self.form_widget = central_widgets.FormWidget(self)
        self.toolbar = self.addToolBar('Main Toolbar')
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('../images/icons/rolling.png'))
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
        export_button.setShortcut("Ctrl+E")
        export_button.setStatusTip("Export as dat file")
        export_button.triggered.connect(self.file_export)
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

        export_button = QAction(QIcon('../images/icons/extract.svg'), 'export File', self)
        export_button.triggered.connect(self.file_export)

        self.play_button = QAction(QIcon('../images/icons/play_circle.svg'), 'PLay Audio', self)
        self.play_button.triggered.connect(self.play_audio)
        self.play_button.setEnabled(False)

        self.pause_button = QAction(QIcon('../images/icons/pause_circle.svg'), 'Pause Audio', self)
        self.pause_button.triggered.connect(self.pause_audio)
        self.pause_button.setEnabled(False)

        self.stop_button = QAction(QIcon('../images/icons/stop_circle.svg'), 'Stop Audio', self)
        self.stop_button.triggered.connect(self.stop_audio)
        self.stop_button.setEnabled(False)

        self.toolbar.addAction(open_button)
        self.toolbar.addAction(export_button)
        self.toolbar.addAction(self.play_button)
        self.toolbar.addAction(self.pause_button)
        self.toolbar.addAction(self.stop_button)

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open File', filter='*.wav', directory='../sounds/')
        if path is not '':
            self.data.open_wav(path)
            filename = path.split('/')
            self.form_widget.plot_data(filename[len(filename) - 1])
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.pause_button.setEnabled(True)

    def file_export(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Export File', filter='*.dat', directory='../out/')
        if path is not '':
            self.data.export_dat(path)

    def play_audio(self):
        self.data.play_audio()
        count = 0
        self.form_widget.draw_vertical_line(self.data.get_current_time(), remove=False, color='g')
        while count < len(self.data.dat) and self.data.get_current_time() != 0.0:
            if self.data.dat[count][0] <= self.data.get_current_index():
                if self.form_widget.radiobutton_is_checked() and True:    # TODO: The 'true' must check condition to see which mouth updates
                    self.form_widget.update_mouth2(self.data.dat[count][1].name)
                else:
                    self.form_widget.update_mouth1(self.data.dat[count][1].name)
                print(str(self.data.dat[count][0]) + ' ' + self.data.dat[count][1].name)
                count = count + 1
            self.form_widget.draw_vertical_line(self.data.get_current_time(), color='g')
            QApplication.processEvents()
        self.form_widget.remove_line()

    def stop_audio(self):
        self.data.stop_audio()

    def pause_audio(self):
        self.form_widget.add_vertical_line(self.data.get_current_time())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
