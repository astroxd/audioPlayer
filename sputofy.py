# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sputofy.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os

from PyQt5.QtWidgets import QStyle
from PyQt5.QtGui import QIcon

gui_base_path = os.path.split(os.path.abspath(__file__))[0]
gui_specific_path = f"{gui_base_path}\\res"


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(675, 626)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 6, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        
        self.playlist1Btn = QtWidgets.QPushButton(self.centralwidget)
        self.playlist1Btn.setObjectName("playlist1Btn")
        self.horizontalLayout_4.addWidget(self.playlist1Btn)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)

        self.playlist2Btn = QtWidgets.QPushButton(self.centralwidget)
        self.playlist2Btn.setObjectName("playlist2Btn")
        self.horizontalLayout_4.addWidget(self.playlist2Btn)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)

        self.playlist3Btn = QtWidgets.QPushButton(self.centralwidget)
        self.playlist3Btn.setObjectName("playlist3Btn")
        self.horizontalLayout_4.addWidget(self.playlist3Btn)
        
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        

        self.playlistView = QtWidgets.QListView(self.centralwidget)
        self.playlistView.setAcceptDrops(True)
        self.playlistView.setProperty("showDropIndicator", True)
        self.playlistView.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.playlistView.setAlternatingRowColors(True)
        self.playlistView.setUniformItemSizes(True)
        self.playlistView.setObjectName("playlistView")
        self.gridLayout_2.addWidget(self.playlistView, 1, 0, 1, 1)


        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 6, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")


        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)


        self.volumeBtn = QtWidgets.QPushButton(self.centralwidget)
        volumeIcon = QtGui.QIcon()
        volumeIcon.addPixmap(QtGui.QPixmap(os.path.join(gui_specific_path, "volumeIcon.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.volumeBtn.setIcon(volumeIcon)
        self.volumeBtn.setObjectName("volumeBtn")
        self.horizontalLayout_3.addWidget(self.volumeBtn)

        
        self.volumeSlider = QtWidgets.QSlider(self.centralwidget)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setFocusPolicy(QtCore.Qt.TabFocus)
        self.volumeSlider.setObjectName("volumeSlider")
        self.horizontalLayout_3.addWidget(self.volumeSlider)

        self.volumeLabel = QtWidgets.QLabel(self.centralwidget)
        self.volumeLabel.setObjectName("volumeLabel")
        self.horizontalLayout_3.addWidget(self.volumeLabel)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 6, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")


        self.time_remainingLabel = QtWidgets.QLabel(self.centralwidget)
        self.time_remainingLabel.setObjectName("time_remainingLabel")
        self.horizontalLayout_2.addWidget(self.time_remainingLabel)


        self.durationSlider = QtWidgets.QSlider(self.centralwidget)
        self.durationSlider.setOrientation(QtCore.Qt.Horizontal)
        self.durationSlider.setFocusPolicy(QtCore.Qt.TabFocus)
        self.durationSlider.setObjectName("durationSlider")
        self.horizontalLayout_2.addWidget(self.durationSlider)


        self.total_timeLabel = QtWidgets.QLabel(self.centralwidget)
        self.total_timeLabel.setObjectName("total_timeLabel")
        self.horizontalLayout_2.addWidget(self.total_timeLabel)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")


        self.loopBtn = QtWidgets.QPushButton(self.centralwidget)
        loopIcon = QtGui.QIcon()
        loopIcon.addPixmap(QtGui.QPixmap(os.path.join(gui_specific_path, "loopIconOFF.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loopBtn.setIcon(loopIcon)
        self.loopBtn.setObjectName("loopBtn")
        self.horizontalLayout.addWidget(self.loopBtn)


        self.prevBtn = QtWidgets.QPushButton(self.centralwidget)
        prevIcon = QtGui.QIcon()
        prevIcon.addPixmap(QtGui.QPixmap(os.path.join(gui_specific_path, "backwardIcon.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prevBtn.setIcon(prevIcon)
        self.prevBtn.setObjectName("prevBtn")
        self.horizontalLayout.addWidget(self.prevBtn)
        # self.prevBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))


        self.playBtn = QtWidgets.QPushButton(self.centralwidget)
        playIcon = QtGui.QIcon()
        playIcon.addPixmap(QtGui.QPixmap(os.path.join(gui_specific_path, "playIcon.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playBtn.setIcon(playIcon)
        self.playBtn.setObjectName("playBtn")
        self.horizontalLayout.addWidget(self.playBtn)
        # self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))


        self.nextBtn = QtWidgets.QPushButton(self.centralwidget)
        nextIcon = QtGui.QIcon()
        nextIcon.addPixmap(QtGui.QPixmap(os.path.join(gui_specific_path, "forwardIcon.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextBtn.setIcon(nextIcon)
        self.nextBtn.setObjectName("nextBtn")
        self.horizontalLayout.addWidget(self.nextBtn)
        # self.nextBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))

        
        self.randomBtn = QtWidgets.QPushButton(self.centralwidget)
        randomIcon = QtGui.QIcon()
        randomIcon.addPixmap(QtGui.QPixmap(os.path.join(gui_specific_path, "randomIconOFF.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.randomBtn.setIcon(randomIcon)
        self.randomBtn.setIconSize(QtCore.QSize(18, 18))
        self.randomBtn.setObjectName("randomBtn")
        self.horizontalLayout.addWidget(self.randomBtn)

        

        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 663, 21))
        self.menubar.setObjectName("menubar")


        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuSong = QtWidgets.QMenu(self.menubar)
        self.menuSong.setObjectName("menuSong")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")


        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_File.setObjectName("actionOpen_File")


        self.actionOpen_Folder = QtWidgets.QAction(MainWindow)
        self.actionOpen_Folder.setObjectName("actionOpen_Folder")

        self.actionOpenSecondWindow = QtWidgets.QAction(MainWindow)
        self.actionOpenSecondWindow.setObjectName("actionOpenSecondWindow")

        self.actionLoopIt = QtWidgets.QAction(MainWindow)
        self.actionLoopIt.setObjectName("actionLoopIt")

        self.actionPlaylist1 = QtWidgets.QAction(MainWindow)
        self.actionPlaylist1.setObjectName("acttionPlaylist1")
        
        self.actionPlaylist2 = QtWidgets.QAction(MainWindow)
        self.actionPlaylist2.setObjectName("acttionPlaylist2")
        
        self.actionPlaylist3 = QtWidgets.QAction(MainWindow)
        self.actionPlaylist3.setObjectName("acttionPlaylist3")

        self.actionDeletePlaylist = QtWidgets.QAction(MainWindow)
        self.actionDeletePlaylist.setObjectName("actionDeletePlaylist")


        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addAction(self.actionOpen_Folder)
        self.menuFile.addAction(self.actionOpenSecondWindow)
        self.menubar.addAction(self.menuFile.menuAction())

        self.menuSong.addAction(self.actionLoopIt)
        self.menuSong.addAction(self.actionPlaylist1)
        self.menuSong.addAction(self.actionPlaylist2)
        self.menuSong.addAction(self.actionPlaylist3)
        self.menuSong.addAction(self.actionDeletePlaylist)
        self.menubar.addAction(self.menuSong.menuAction())
        
        
        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.playBtn.setText(_translate("MainWindow", ""))
        self.nextBtn.setText(_translate("MainWindow", ""))
        self.prevBtn.setText(_translate("MainWindow", ""))
        self.randomBtn.setText(_translate("MainWindow",""))
        self.loopBtn.setText(_translate("MainWindow", ""))
        self.volumeBtn.setText(_translate("MainWindow", ""))


        self.time_remainingLabel.setText(_translate("MainWindow", "00:00"))
        self.total_timeLabel.setText(_translate("MainWindow", "00:00"))
        self.volumeLabel.setText(_translate("MainWindow", "100%"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))

        self.actionOpen_File.setText(_translate("MainWindow", "Open File"))
        self.actionOpen_File.setShortcut(_translate("MainWindow", "Ctrl+O"))


        self.actionOpen_Folder.setText(_translate("MainWindow", "Open Folder"))
        self.actionOpen_Folder.setShortcut(_translate("MainWindow", "Ctrl+F"))


        self.actionOpenSecondWindow.setText(_translate("MainWindow","Open Second Window"))
        self.actionOpenSecondWindow.setShortcut(_translate("MainWindow", "Ctrl+T"))


        self.menuSong.setTitle(_translate("MainWindo", "Song"))

        self.actionLoopIt.setText(_translate("MainWindow", "Loop it: OFF"))
        self.actionLoopIt.setShortcut(_translate("MainWindow", "Ctrl+L"))

        self.actionPlaylist1.setText(_translate("MainWindow", "Playlist 1"))
        self.actionPlaylist2.setText(_translate("MainWindow", "Playlist 2"))
        self.actionPlaylist3.setText(_translate("MainWindow", "Playlist 3"))
        self.actionDeletePlaylist.setText(_translate("MainWindow", "Delete Playlist"))
        
        self.playlist1Btn.setText(_translate("MainWindow", "P1"))
        self.playlist2Btn.setText(_translate("MainWindow", "P2"))
        self.playlist3Btn.setText(_translate("MainWindow", "P3"))
        