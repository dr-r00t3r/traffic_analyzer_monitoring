from __future__ import unicode_literals
import ast
import sys
import os

import threading

from matplotlib.backends import qt_compat

use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    pass
    # from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

        self.timeToStart = None
        self.MAXITERS = None
        self.before = None
        self.keys = None
        self.dicLengthData = {}
        self.dicCounterRequest = {}
        self.dicTimeForPerRequest = {}
        # self.fig = Figure()
        # self.ax = self.fig.add_subplot(111)
        self.ax.set_ylabel('Length Data Request ')
        self.ax.set_xlabel('Time per Request')
        self.ax.grid(True)
        # FigureCanvas.__init__(self, self.fig).__init__(self.par)
        self.ax.set_autoscale_on(False)
        self.cnt = 0
        self.l = {}

    def prepareData(self, obj, t):
        self.timeToStart = t
        self.ax.set_xlim(0, 500)
        self.ax.set_ylim(0, 500)

        self.keys = obj.dicCounterRequest.keys()
        li = len(self.keys)
        for i in self.keys:
            if self.dicLengthData.has_key(i):
                self.dicLengthData[i] = obj.dicLengthData[i]
            else:
                self.dicLengthData[i] = []
                # string = i + " : " + obj.dicIPHostName[i]
                # print obj.dicIPHostName[i]
                string = i.__str__() + " " + obj.dicIPHostName[i].__str__()
                self.l[i], = self.ax.plot([], label=string)
                self.dicLengthData[i] = obj.dicLengthData[i]

            self.dicTimeForPerRequest[i] = []
            for j in obj.dicTimeForPerRequest[i]:
                self.dicTimeForPerRequest[i].append(
                    (ast.literal_eval(j.__str__()) - ast.literal_eval(self.timeToStart.__str__())) / 1000)
                # self.dicTimeForPerRequest[i] = obj.dicTimeForPerRequest[i]
                # print ls.__str__()[-8:]
                # self.l_dicCounterRequest[i].set_data(self.dicCounterRequest[i], obj.dicTimeForPerRequest[i])
                # self.dicCounterRequest[i] = obj.dicCounterRequest[i]
        # self.fig
        # print self.dicCounterRequest, self.dicTimeForPerRequest
        self.ax.legend()

        for i in self.keys:
            (self.l[i]).set_data(self.dicTimeForPerRequest[i], self.dicLengthData[i])
            # lis = self.l[i].set_data(self.dicCounterRequest[i], self.dicTimeForPerRequest[i] )
            # lis.set_data(self.dicCounterRequest[i], self.dicTimeForPerRequest[i] )
            # self.ax.legend()
        # self.ax.annotate("2001 Census", xy=(250, 100), xytext=(0, 0), arrowprops=dict(arrowstyle='fancy'))
        self.fig.canvas.draw()
        # self.fig.canvas.draw()


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

        self.timeToStart = None
        self.MAXITERS = None
        self.before = None
        self.keys = None
        self.dicTimeForPerRequest = {}
        self.dicCounterRequest = {}
        self.l_dicCounterRequest = {}
        # self.fig = Figure()
        # self.ax = self.fig.add_subplot(111)
        self.ax.set_ylabel('IP Per Request ')
        self.ax.set_xlabel('Time per Request')
        self.ax.grid(True)
        # FigureCanvas.__init__(self, self.fig).__init__(self.par)
        self.ax.set_autoscale_on(False)
        self.cnt = 0
        self.l = {}

    def prepareData(self, obj, t):
        self.timeToStart = t
        self.ax.set_xlim(0, 500)
        self.ax.set_ylim(0, 1000)

        """helper function to return CPU usage info"""
        self.keys = obj.dicCounterRequest.keys()
        li = len(self.keys)
        for i in self.keys:
            if self.dicCounterRequest.has_key(i):
                self.dicCounterRequest[i] = obj.dicCounterRequest[i]
            else:
                self.dicCounterRequest[i] = []
                # string = i + " : " + obj.dicIPHostName[i]
                # print obj.dicIPHostName[i]
                string = i.__str__() + " " + obj.dicIPHostName[i].__str__()
                self.l[i], = self.ax.plot([], label=string)
                self.dicCounterRequest[i] = obj.dicCounterRequest[i]
            self.dicTimeForPerRequest[i] = []
            for j in obj.dicTimeForPerRequest[i]:
                self.dicTimeForPerRequest[i].append(
                    (ast.literal_eval(j.__str__()) - ast.literal_eval(self.timeToStart.__str__())) / 1000)
                # self.dicTimeForPerRequest[i] = obj.dicTimeForPerRequest[i]
                # print ls.__str__()[-8:]
                # self.l_dicCounterRequest[i].set_data(self.dicCounterRequest[i], obj.dicTimeForPerRequest[i])
                # self.dicCounterRequest[i] = obj.dicCounterRequest[i]
        # self.fig
        # print self.dicCounterRequest, self.dicTimeForPerRequest
        self.ax.legend()

        for i in self.keys:
            (self.l[i]).set_data(self.dicTimeForPerRequest[i], self.dicCounterRequest[i])
            # (self.l[i]).set_text("asdfasd")
            # self.l[i].clabel(1)
            # lis = self.l[i].set_data(self.dicCounterRequest[i], self.dicTimeForPerRequest[i] )
            # lis.set_data(self.dicCounterRequest[i], self.dicTimeForPerRequest[i] )
            # self.ax.legend()
        # self.ax.annotate("2001 Census", xy=(250, 100), xytext=(0, 0), arrowprops=dict(arrowstyle='fancy'))
        self.fig.canvas.draw()
        # self.fig.canvas.draw()


class AnaliyzMain(QtGui.QMainWindow):
    def __init__(self, ob):
        QtGui.QMainWindow.__init__(self).__init__(ob)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.firstExecuted = False
        self.resize(2048, 1536)
        self.setWindowIcon(QtGui.QIcon('asset/Icon.png'))
        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)
        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)
        self.help_menu.addAction('&About', self.about)
        self.main_widget = QtGui.QWidget(self)
        l = QtGui.QVBoxLayout(self.main_widget)
        self.sc = MyStaticMplCanvas(self.main_widget, width=10, height=7, dpi=100)
        self.dc = MyDynamicMplCanvas(self.main_widget, width=10, height=7, dpi=100)
        l.addWidget(self.sc)
        l.addWidget(self.dc)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def excuted(self, obj, t):
        if not self.firstExecuted:
            self.setWindowTitle((obj.IPDevice[0] + "." + obj.IPDevice[1] + "." + obj.IPDevice[2] + "." + "*").__str__())
            self.firstExecuted = True
        else:
            pass

        T1 = threading.Thread(self.sc.prepareData(obj, t))
        T2 = threading.Thread(self.dc.prepareData(obj, t))
        T1.start()
        # T1.join()
        T2.start()
        # T2.join()

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtGui.QMessageBox.about(self, "About",
                                """embedding_in_qt4.py example
                                    Copyright 2005 Florent Rougon, 2006 Darren Dale
                                    This program is a simple example of a Qt4 application embedding matplotlib canvases.
                                    It may be used and modified with no restriction; raw copies as well as
                                    modified versions may be distributed without limitation."""
                                )
