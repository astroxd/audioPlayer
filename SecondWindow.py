# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fourthWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(407, 131)
        
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # playlist/video link from youtube
        self.youtube_link = QtWidgets.QLineEdit(Dialog)
        self.youtube_link.setObjectName("youtube_link")
        self.horizontalLayout.addWidget(self.youtube_link)
        
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        
        # path where songs will be downloaded
        self.download_folder = QtWidgets.QLineEdit(Dialog)
        self.download_folder.setObjectName("download_folder")
        self.horizontalLayout_2.addWidget(self.download_folder)
        
        
        # button for open the file explorer
        self.download_folderBtn = QtWidgets.QPushButton(Dialog)
        self.download_folderBtn.setObjectName("download_folderBtn")
        self.horizontalLayout_2.addWidget(self.download_folderBtn)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        
        
        # button for start downloading the songs
        self.startBtn = QtWidgets.QPushButton(Dialog)
        self.startBtn.setObjectName("startBtn")
        self.gridLayout.addWidget(self.startBtn, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.download_folderBtn.setText(_translate("Dialog", "Folder"))
        self.startBtn.setText(_translate("Dialog", "Start"))
        self.youtube_link.setPlaceholderText(_translate("Dialog","e.g  https://youtu.be/a4eqgjtMGSI"))
        self.download_folder.setPlaceholderText(_translate("Dialog","e.g  C:/Download"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())