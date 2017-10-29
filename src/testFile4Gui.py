#!/usr/bin/env python

"""
@author: Diego Castaneda (dfcastap@gmail.com)

This script creates a basic GUI

Based on http://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
"""

from __future__ import unicode_literals
import sys
import os
import matplotlib

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

import numpy as np
import pylab as plt

# Load matplotlib Qt stuff:
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# Set a name to out program based on its filename:
progname = os.path.basename(sys.argv[0])



class plotCanvas(FigureCanvas):
    """Simple canvas with a sine plot."""

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi,facecolor="white")
        self.axes = fig.add_subplot(111)
        #self.make_contour("/home/castaned/Documents/code_lab/qt/c_data.dat")

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.axes.axis('off')

    def make_contour(self,fname):
        """
            Loads the file at fname and plots its contents. It uses
            matplotlib's contourf function to plot X, Y, Z contained in
            the file. Each coordinate is expected to be a meshgrid.
        """
        data = np.genfromtxt(fname)
        l = len(data[:,0])/3
        x = data[0:l,:]
        y = data[l:2*l,:]
        z = data[2*l:3*l,:]

        self.axes.contourf(x,y,z, 100, cmap=plt.cm.gnuplot,
                                              vmax=np.max(z), vmin=np.min(z))
        self.axes.contourf(x,-y,z, 100, cmap=plt.cm.gnuplot,
                                              vmax=np.max(z), vmin=np.min(z))
        self.axes.contourf(-x,-y,z, 100, cmap=plt.cm.gnuplot,
                                              vmax=np.max(z), vmin=np.min(z))
        self.axes.contourf(-x,y,z, 100, cmap=plt.cm.gnuplot,
                                              vmax=np.max(z), vmin=np.min(z))

        self.draw()



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """
            Setup the main window with Qt widgets
        """
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Plot - countourf")
        self.main_widget = QtWidgets.QWidget(self)

        # Box will contain the elements we want to include in a vertical
        # layout.

        box = QtWidgets.QVBoxLayout(self.main_widget)

        # Init. the plotCanvas class and add the Matplotlib toolbar:
        self.sc = plotCanvas(self.main_widget, width=5, height=5, dpi=100)
        mpl_toolbar = NavigationToolbar(self.sc, self.main_widget)



        # Add a nice menu bar to open a file to plot and exit options:
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction('&Open', self.filePick,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        fileMenu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)

        # Add the Qt widgets to the main window
        box.addWidget(self.sc)
        box.addWidget(mpl_toolbar)

        # Set the focus on the main widget:
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def filePick(self):
        """
            Generic code for a file picker. In this case
            once a file is selected, the directory of the file is passed
            to the make_contour function on the plotCanvas class for
            plotting.
        """
        curr_path = os.getcwd()
        fname = QtWidgets.QFileDialog.getOpenFileName(self,
                                                      'Open file', curr_path)

        if fname[0]:
            self.sc.make_contour(fname[0])


    def fileQuit(self):
        """
            Exit the application
        """
        self.close()


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
