# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SputofyGui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(840, 603)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
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
        self.volumeBtn.setText("")
        self.volumeBtn.setObjectName("volumeBtn")
        self.horizontalLayout_3.addWidget(self.volumeBtn)
        self.volumeSlider = QtWidgets.QSlider(self.centralwidget)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.horizontalLayout_3.addWidget(self.volumeSlider)
        self.volumeLabel = QtWidgets.QLabel(self.centralwidget)
        self.volumeLabel.setObjectName("volumeLabel")
        self.horizontalLayout_3.addWidget(self.volumeLabel)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loopBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loopBtn.setText("")
        self.loopBtn.setObjectName("loopBtn")
        self.horizontalLayout.addWidget(self.loopBtn)
        self.prevBtn = QtWidgets.QPushButton(self.centralwidget)
        self.prevBtn.setText("")
        self.prevBtn.setObjectName("prevBtn")
        self.horizontalLayout.addWidget(self.prevBtn)
        self.playBtn = QtWidgets.QPushButton(self.centralwidget)
        self.playBtn.setText("")
        self.playBtn.setObjectName("playBtn")
        self.horizontalLayout.addWidget(self.playBtn)
        self.nextBtn = QtWidgets.QPushButton(self.centralwidget)
        self.nextBtn.setText("")
        self.nextBtn.setObjectName("nextBtn")
        self.horizontalLayout.addWidget(self.nextBtn)
        self.randomBtn = QtWidgets.QPushButton(self.centralwidget)
        self.randomBtn.setText("")
        self.randomBtn.setObjectName("randomBtn")
        self.horizontalLayout.addWidget(self.randomBtn)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.elapsedTime_Label = QtWidgets.QLabel(self.centralwidget)
        self.elapsedTime_Label.setObjectName("elapsedTime_Label")
        self.horizontalLayout_2.addWidget(self.elapsedTime_Label)
        self.durationSlider = QtWidgets.QSlider(self.centralwidget)
        self.durationSlider.setOrientation(QtCore.Qt.Horizontal)
        self.durationSlider.setObjectName("durationSlider")
        self.horizontalLayout_2.addWidget(self.durationSlider)
        self.totalTime_Label = QtWidgets.QLabel(self.centralwidget)
        self.totalTime_Label.setObjectName("totalTime_Label")
        self.horizontalLayout_2.addWidget(self.totalTime_Label)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.playlistView = QtWidgets.QListWidget(self.centralwidget)
        self.playlistView.setObjectName("playlistView")
        self.gridLayout_2.addWidget(self.playlistView, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 840, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setToolTipsVisible(True)
        self.menuFile.setObjectName("menuFile")
        self.menuSong = QtWidgets.QMenu(self.menubar)
        self.menuSong.setToolTipsVisible(True)
        self.menuSong.setObjectName("menuSong")
        self.menuPlaylist = QtWidgets.QMenu(self.menubar)
        self.menuPlaylist.setObjectName("menuPlaylist")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Song = QtWidgets.QAction(MainWindow)
        self.actionOpen_Song.setObjectName("actionOpen_Song")
        self.actionOpen_Folder = QtWidgets.QAction(MainWindow)
        self.actionOpen_Folder.setObjectName("actionOpen_Folder")
        self.actionYT_MP3 = QtWidgets.QAction(MainWindow)
        self.actionYT_MP3.setObjectName("actionYT_MP3")
        self.actionLoopIt = QtWidgets.QAction(MainWindow)
        self.actionLoopIt.setObjectName("actionLoopIt")
        self.actionShuffle = QtWidgets.QAction(MainWindow)
        self.actionShuffle.setObjectName("actionShuffle")
        self.actionCreatePlaylist = QtWidgets.QAction(MainWindow)
        self.actionCreatePlaylist.setObjectName("actionCreatePlaylist")
        self.actionDeletePlaylist = QtWidgets.QAction(MainWindow)
        self.actionDeletePlaylist.setObjectName("actionDeletePlaylist")
        self.menuFile.addAction(self.actionOpen_Song)
        self.menuFile.addAction(self.actionOpen_Folder)
        self.menuFile.addAction(self.actionYT_MP3)
        self.menuSong.addAction(self.actionLoopIt)
        self.menuSong.addAction(self.actionShuffle)
        self.menuSong.addSeparator()
        self.menuSong.addAction(self.actionCreatePlaylist)
        self.menuSong.addAction(self.actionDeletePlaylist)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSong.menuAction())
        self.menubar.addAction(self.menuPlaylist.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.volumeBtn.setToolTip(_translate("MainWindow", "Mute/Unmute Volume"))
        self.volumeBtn.setShortcut(_translate("MainWindow", "M"))
        self.volumeLabel.setText(_translate("MainWindow", "100%"))
        self.loopBtn.setToolTip(_translate("MainWindow", "Repeat all songs"))
        self.loopBtn.setShortcut(_translate("MainWindow", "L"))
        self.prevBtn.setToolTip(_translate("MainWindow", "Back to previous song"))
        self.prevBtn.setShortcut(_translate("MainWindow", "A"))
        self.playBtn.setToolTip(_translate("MainWindow", "Play/Pause song"))
        self.playBtn.setShortcut(_translate("MainWindow", "Space"))
        self.nextBtn.setToolTip(_translate("MainWindow", "Skip to next song"))
        self.nextBtn.setShortcut(_translate("MainWindow", "D"))
        self.randomBtn.setToolTip(_translate("MainWindow", "Play random song"))
        self.randomBtn.setShortcut(_translate("MainWindow", "R"))
        self.elapsedTime_Label.setText(_translate("MainWindow", "00:00"))
        self.totalTime_Label.setText(_translate("MainWindow", "00:00"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSong.setTitle(_translate("MainWindow", "Song"))
        self.menuPlaylist.setTitle(_translate("MainWindow", "Playlist"))
        self.actionOpen_Song.setText(_translate("MainWindow", "Open Song"))
        self.actionOpen_Song.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionOpen_Folder.setText(_translate("MainWindow", "Open Folder"))
        self.actionOpen_Folder.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.actionYT_MP3.setText(_translate("MainWindow", "YouTube to MP3"))
        self.actionYT_MP3.setToolTip(_translate("MainWindow", "Convert Youtube link to MP3 file"))
        self.actionYT_MP3.setShortcut(_translate("MainWindow", "Ctrl+T"))
        self.actionLoopIt.setText(_translate("MainWindow", "Loop it: OFF"))
        self.actionLoopIt.setToolTip(_translate("MainWindow", "Repeat current song"))
        self.actionLoopIt.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.actionShuffle.setText(_translate("MainWindow", "Shuffle"))
        self.actionShuffle.setToolTip(_translate("MainWindow", "Change song\'s order"))
        self.actionShuffle.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionCreatePlaylist.setText(_translate("MainWindow", "Playlist This"))
        self.actionCreatePlaylist.setToolTip(_translate("MainWindow", "Create playlist using current songs"))
        self.actionDeletePlaylist.setText(_translate("MainWindow", "Delete Playlist"))
        self.actionDeletePlaylist.setToolTip(_translate("MainWindow", "Delete current playlist"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())