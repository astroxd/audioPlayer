# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sputofy.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(663, 430)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(55, 11, 551, 211))
        self.textBrowser.setObjectName("textBrowser")


        self.durationSlider = QtWidgets.QSlider(self.centralwidget)
        self.durationSlider.setGeometry(QtCore.QRect(60, 310, 351, 22))
        self.durationSlider.setOrientation(QtCore.Qt.Horizontal)
        self.durationSlider.setRange(0,0)
        self.durationSlider.setObjectName("durationSlider")


        self.playBtn = QtWidgets.QPushButton(self.centralwidget)
        self.playBtn.setGeometry(QtCore.QRect(320, 260, 31, 31))
        self.playBtn.setObjectName("playBtn")


        self.nextBtn = QtWidgets.QPushButton(self.centralwidget)
        self.nextBtn.setGeometry(QtCore.QRect(410, 260, 31, 31))
        self.nextBtn.setObjectName("nextBtn")


        self.prevBtn = QtWidgets.QPushButton(self.centralwidget)
        self.prevBtn.setGeometry(QtCore.QRect(230, 260, 31, 31))
        self.prevBtn.setObjectName("prevBtn")

        self.shuffleBtn = QtWidgets.QPushButton(self.centralwidget)
        # self.shuffleBtn.setGeometry(QtCore.QRect(310, 360, 160, 21))
        self.shuffleBtn.setObjectName("shuffleBtn")


        self.loopBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loopBtn.setGeometry(QtCore.QRect(180, 360, 160, 21))
        self.loopBtn.setObjectName("loopBtn")



        self.volumeSlider = QtWidgets.QSlider(self.centralwidget)
        self.volumeSlider.setGeometry(QtCore.QRect(500, 310, 101, 22))
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setObjectName("volumeSlider")


        self.volumeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.volumeBtn.setGeometry(QtCore.QRect(470, 310, 21, 23))
        self.volumeBtn.setObjectName("volumeBtn")


        self.time_remainingLabel = QtWidgets.QLabel(self.centralwidget)
        self.time_remainingLabel.setGeometry(QtCore.QRect(19, 310, 31, 20))
        self.time_remainingLabel.setObjectName("time_remainingLabel")


        self.total_timeLabel = QtWidgets.QLabel(self.centralwidget)
        self.total_timeLabel.setGeometry(QtCore.QRect(420, 310, 31, 21))
        self.total_timeLabel.setGeometry(QtCore.QRect(310, 360, 160, 21)) #TODO
        self.total_timeLabel.setObjectName("total_timeLabel")


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 663, 21))
        self.menubar.setObjectName("menubar")


        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")


        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")


        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_File.setObjectName("actionOpen_File")


        self.actionOpen_Folder = QtWidgets.QAction(MainWindow)
        self.actionOpen_Folder.setObjectName("actionOpen_Folder")


        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addAction(self.actionOpen_Folder)
        self.menubar.addAction(self.menuFile.menuAction())


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.playBtn.setText(_translate("MainWindow", ""))
        self.nextBtn.setText(_translate("MainWindow", "2"))
        self.prevBtn.setText(_translate("MainWindow", "3"))
        self.shuffleBtn.setText(_translate("MainWindow","5"))
        self.loopBtn.setText(_translate("MainWindow", "6"))
        self.volumeBtn.setText(_translate("MainWindow", ""))
        self.time_remainingLabel.setText(_translate("MainWindow", "00:00"))
        self.total_timeLabel.setText(_translate("MainWindow", "00:00"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_File.setText(_translate("MainWindow", "Open File"))
        self.actionOpen_Folder.setText(_translate("MainWindow", "Open Folder"))

