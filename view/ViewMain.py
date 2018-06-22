# -*- coding: utf-8 -*-
import sys
import time
from netifaces import ifaddresses, AF_INET

import pyautogui
import winreg as wr
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread, SIGNAL, pyqtSlot, QObject, SLOT
from PyQt4.QtGui import *

from analyzer.AnalyzerMain import AnaliyzMain
# from interface_sniff.LocalSniffer import LocalSniffer
from interface_sniff.LocalSniffer import LocalSniffer
from iostream.IOStreamMain import IOStreamMain
from view.ChaildView import ChaildView

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def enviromentDesktop(self):
        self.scx, self.scy = pyautogui.size()
        self.widthSize = (3 * self.scx) / 4
        self.hiegthSize = (3 * self.scy) / 4
        self.scale = 0.75

    def setupUi(self, MainWindow):
        self.enviromentDesktop()
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        # palette = QtGui.QPalette()
        # palette.setColor(QtGui.QPalette.Background, QtCore.Qt.red)
        # MainWindow.setPalette(palette)
        MainWindow.resize(self.widthSize, self.hiegthSize)
        MainWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0.02 * self.widthSize, 10, 1200, 90))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.itemSelect = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.itemSelect.setObjectName(_fromUtf8("ItemSelect"))
        self.horizontalLayout.addWidget(self.itemSelect)
        self.btnMonitoring = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnMonitoring.setObjectName(_fromUtf8("btnMonitoring"))
        self.horizontalLayout.addWidget(self.btnMonitoring)
        self.btnStop = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnStop.setObjectName(_fromUtf8("btnStop"))
        self.btnStop.setVisible(False)
        self.horizontalLayout.addWidget(self.btnStop)
        self.tableView = MyTableView(self.centralwidget)
        self.tableView.setGeometry(
            QtCore.QRect(0.025 * self.widthSize, 0.1 * self.hiegthSize, 0.95 * self.widthSize, 0.80 * self.hiegthSize))
        # self.tableView.setHorizontalHeader(QHeaderView(Qt.Horizontal, self.tableView))
        self.headers = ["time", "Source IP", "Destination IP", "Protocol", "Length", "Info"]
        self.model = QStandardItemModel()
        self.model.setColumnCount(5)
        self.model.setHorizontalHeaderLabels(self.headers)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(0, 200)
        self.tableView.setColumnWidth(1, 400)
        self.tableView.setColumnWidth(2, 400)
        self.tableView.setColumnWidth(3, 150)
        self.tableView.setColumnWidth(4, 150)
        self.tableView.setColumnWidth(5, 800)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setShortcut(QKeySequence("Ctrl+N"))
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setShortcut(QKeySequence("Ctrl+Q"))
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionFullScreen = QtGui.QAction(MainWindow)
        self.actionFullScreen.setShortcut(QKeySequence("Ctrl+F"))
        self.actionFullScreen.setObjectName(_fromUtf8("actionFullScreen"))
        self.actionOption = QtGui.QAction(MainWindow)
        self.actionOption.setObjectName(_fromUtf8("actionOption"))
        self.actionTelnet = QtGui.QAction(MainWindow)
        self.actionTelnet.setObjectName(_fromUtf8("actionTelnet"))
        self.actionHTTP = QtGui.QAction(MainWindow)
        self.actionHTTP.setObjectName(_fromUtf8("actionHTTP"))
        self.actionDocument = QtGui.QAction(MainWindow)
        self.actionDocument.setObjectName(_fromUtf8("actionDocument"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionExit)
        self.menuView.addAction(self.actionFullScreen)
        self.menuTools.addAction(self.actionTelnet)
        self.menuTools.addAction(self.actionHTTP)
        self.menuTools.addAction(self.actionOption)
        self.menuAbout.addAction(self.actionDocument)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        MainWindow.setWindowIcon(QtGui.QIcon('asset/Icon.png'))
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Trafice and  Analyz and monitoring", None))
        self.btnMonitoring.setText(_translate("MainWindow", "Monitoring", None))
        self.btnStop.setText(_translate("MainWindow", "Stop", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuView.setTitle(_translate("MainWindow", "View", None))
        self.menuTools.setTitle(_translate("MainWindow", "tools", None))
        self.menuAbout.setTitle(_translate("MainWindow", "About", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionFullScreen.setText(_translate("MainWindow", "FullScreen", None))
        self.actionOption.setText(_translate("MainWindow", "Option", None))
        self.actionTelnet.setText(_translate("MainWindow", "Telnet", None))
        self.actionHTTP.setText(_translate("MainWindow", "HTTP", None))
        self.actionDocument.setText(_translate("MainWindow", "Document", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))

    def initialTableView(self):
        self.model.setColumnCount(5)
        self.model.setHorizontalHeaderLabels(self.headers)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(0, 200)
        self.tableView.setColumnWidth(1, 400)
        self.tableView.setColumnWidth(2, 400)
        self.tableView.setColumnWidth(3, 150)
        self.tableView.setColumnWidth(4, 150)
        self.tableView.setColumnWidth(5, 800)


class ViewMain(QtGui.QMainWindow, Ui_MainWindow):
    nameItemSelected = None
    Object = None
    lPacketView = []

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.boolControl = 0
        self.controlFullScreen = False
        self.listDeviceName = {}
        self.listIpDevice = {}
        self.setupUi(self)
        self.snifferObject = LocalSniffer()
        self.getNetWorkDevice()
        self.analiyzMainObject = None
        self.IOStreamMainObject = None
        self.snifferThread = SinfferDoBackground(self.snifferObject)
        self.btnMonitoring.clicked.connect(self.Monitoring)
        self.btnStop.clicked.connect(self.btn_Stop)
        self.snifferObject.ObjectUpdated.connect(self.updateUIAfterMonitoring)
        QObject.connect(self.tableView, SIGNAL("doubleClicked(QModelIndex)"), self.tableView,
                        SLOT("ItemDoubleClicked(QModelIndex)"))
        QObject.connect(self.actionNew, SIGNAL("triggered()"), self, SLOT("actNew()"))
        QObject.connect(self.actionExit, SIGNAL("triggered()"), self, SLOT("actExit()"))
        QObject.connect(self.actionFullScreen, SIGNAL("triggered()"), self, SLOT("actFullScreen()"))
        QObject.connect(self.actionDocument, SIGNAL("triggered()"), self, SLOT("actDocument()"))
        QObject.connect(self.actionAbout, SIGNAL("triggered()"), self, SLOT("actAbout()"))
        # QObject.connect(self.actionNew, SIGNAL("triggered()"), self, SLOT("self.actNew()"))
        # self.actionNew.triggered.connect(self.actionNew)
        # self.actionFullScreen.triggered.connect(self.actionFullScreen)
        # self.actionAbout.triggered.connect(self.actAbout)
        self.listPacket = []
        self.listPacketView = []

    def getNetWorkDevice(self):
        listDevice = self.snifferObject.initializObject()
        for i in range(len(listDevice)):
            j = listDevice[i].split('_')
            reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
            reg_key = wr.OpenKey(reg,
                                 r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
            reg_subkey = wr.OpenKey(reg_key, j[1] + r'\Connection')
            k = wr.QueryValueEx(reg_subkey, 'Name')[0]
            self.listDeviceName[listDevice[i]] = k.__str__()
            addresses = [k['addr'] for k in ifaddresses(j[1]).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
            self.listIpDevice[listDevice[i]] = addresses[0]
        # print (self.listIpDevice)
        self.itemSelect.addItems(self.listDeviceName.values())

    def getSpainItem(self):
        text = self.itemSelect.currentText().__str__()
        for key, name in self.listDeviceName.iteritems():
            if name == text:  # self.listDeviceName[key]=name
                # print key + " " + self.listDeviceName[key]
                ViewMain.nameItemSelected = key
                self.devicename = [key, name]

    def Monitoring(self):
        ViewMain.Object = self

        if self.boolControl == 0:
            self.btnStop.setVisible(True)
            self.getSpainItem()
            self.snifferObject.setterGetterPacketSniff.IPDevice = self.listIpDevice[self.devicename[0]]
            self.snifferObject.setterGetterPacketSniff.getSubnetMaskANDIPRnage()
            self.timeToStart = int(round(time.time() * 1000))
            self.snifferThread.start()
            self.analiyzMainObject = AnaliyzMain(self)
            self.analiyzMainObject.show()
        elif self.boolControl == 1:
            choice = QtGui.QMessageBox.question(self, 'Alert', "Aya save shavad?",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:
                """ open browser and save data """
                self.fileDialog = QtGui.QFileDialog(self)
                while True:
                    self.getString = self.fileDialog.getSaveFileName(self)
                    self.IOStreamMainObject = IOStreamMain(ViewMain.lPacketView, self.getString.__str__())
                    if self.IOStreamMainObject.check():
                        break
                self.IOStreamMainObject.save()
                self.listPacket = []
                self.listPacketView = []
                self.model.clear()
                self.initialTableView()
                self.btnStop.setVisible(True)
                self.getSpainItem()
                self.snifferObject.setterGetterPacketSniff.IPDevice = self.listIpDevice[self.devicename[0]]
                self.snifferObject.setterGetterPacketSniff.getSubnetMaskANDIPRnage()
                self.timeToStart = int(round(time.time() * 1000))
                self.snifferThread.start()
                self.analiyzMainObject = AnaliyzMain(self)
                self.analiyzMainObject.show()
            else:
                self.listPacket = []
                self.listPacketView = []
                self.model.clear()
                self.initialTableView()
                self.btnStop.setVisible(True)
                self.getSpainItem()
                self.snifferObject.setterGetterPacketSniff.IPDevice = self.listIpDevice[self.devicename[0]]
                self.snifferObject.setterGetterPacketSniff.getSubnetMaskANDIPRnage()
                self.timeToStart = int(round(time.time() * 1000))
                self.snifferThread.start()
                self.analiyzMainObject = AnaliyzMain(self)
                self.analiyzMainObject.show()

    def updateUIAfterMonitoring(self, value):
        if value.Checked_Protocol is None or value.Ip_Header_SourceAddress is None:
            pass
        else:
            value.generatPacketString()
            value.setCounterSourceIp()
            try:
                self.analiyzMainObject.excuted(value, self.timeToStart)
            except:
                pass
            ViewMain.lPacketView.append(value)
            self.listPacketView.append(
                [value.timeOFGeneratePacket.__str__()[-8:], value.Ip_Header_SourceAddress.__str__(),
                 value.Ip_Header_DestinationAddress.__str__(),
                 value.Checked_Protocol.__str__(), value.lengthData.__str__(), value.data.__str__()])
            for d in self.listPacketView:
                row = []
                for name in d:
                    item = QStandardItem(name)
                    item.setEditable(False)
                    row.append(item)
                self.model.appendRow(row)
            self.tableView.setModel(self.model)

    def btn_Stop(self):
        self.snifferThread.terminate()
        self.boolControl = 1
        self.btnStop.setVisible(False)

    @pyqtSlot()
    def actNew(self):
        dialog = ViewMain(self)
        dialog.show()

    @pyqtSlot()
    def actExit(self):
        exit()

    @pyqtSlot()
    def actFullScreen(self):
        if not self.controlFullScreen:
            self.move(0, 0)
            self.resize(self.scx, self.scy)
            self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0.02 * self.scx, 10, 1200, 90))
            self.tableView.setGeometry(
                QtCore.QRect(0.025 * self.scx, 0.1 * self.scy, 0.95 * self.scx, 0.80 * self.scy))
            self.controlFullScreen = True

        else:
            self.move(0, 0)
            self.resize(self.widthSize, self.hiegthSize)
            self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0.02 * self.widthSize, 10, 1200, 90))
            self.tableView.setGeometry(
                QtCore.QRect(0.025 * self.widthSize, 0.1 * self.hiegthSize, 0.95 * self.widthSize,
                             0.80 * self.hiegthSize))
            self.controlFullScreen = False

    @pyqtSlot()
    def actTelnet(self):
        pass

    @pyqtSlot()
    def actHTTP(self):
        pass

    @pyqtSlot()
    def actOption(self):
        pass

    @pyqtSlot()
    def actDocument(self):
        pass

    @pyqtSlot()
    def actAbout(self):
        QMessageBox.about(self, "About", " trafice_analyz_monitoring  \n Version 1 \n PyQT 4.1 , Python 2.7 ")


class SinfferDoBackground(QThread):
    def __init__(self, object):
        QThread.__init__(self)
        self.obj = object  # self.obj=>self.snifferObject=>Localsniffer()

    def __del__(self):
        self.wait()

    def run(self):
        self.obj.choiceDevice = ViewMain.nameItemSelected
        self.obj.main(sys.argv)


class MyTableView(QTableView):
    @pyqtSlot("QModelIndex")
    def ItemDoubleClicked(self, index):
        lcontrol = index.row()
        viewBox = ChaildView(ViewMain.lPacketView[lcontrol].packetString, ViewMain.Object)
        viewBox.show()


def main():
    app = QApplication(sys.argv)
    dialog = ViewMain()
    dialog.show()
    app.exec_()
