
from __future__ import unicode_literals

import datetime
import os
import random
import sys

import yaml
import youtube_dl
from mutagen.mp3 import MP3
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QAbstractListModel, Qt, QTimer, QUrl, QEvent
from PyQt5.QtGui import QIcon, QMoveEvent, QCloseEvent
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimedia import (QMediaContent, QMediaPlayer,
                                QMediaPlayerControl, QMediaPlaylist)
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout, QLineEdit, QMainWindow,
                             QPushButton, QStyle, QVBoxLayout)

from SecondWindow import Ui_Dialog
from sputofy import Ui_MainWindow


def yaml_loader():
    with open("audioPlayer/config.yaml", "r") as config:
        data = yaml.load(config, Loader=yaml.FullLoader)
        return data

def yaml_dump(data):
    with open("audioPlayer/config.yaml", "w") as config:
        yaml.dump(data, config)

class config():
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.data = yaml_loader()
        self.default_folder()
        self.last_window_size()

    def default_folder(self):
        user = os.getlogin()
        default_folderConfig = {
            "default_folder": "C:\\Users\\"+user+"\\Desktop\\sputofy_songs"}
        yaml_dump(default_folderConfig)

    def last_window_size(self):
        self.data['last_window_size']['heigth'] = self.height
        self.data['last_window_size']['width'] = self.width
        yaml_dump(self.data)  # TODO è gia nella main window

class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            song = media.canonicalUrl().fileName().replace(".mp3","")
            songPosition = f"{index.row()+1}  {song}"
            # return media.canonicalUrl().fileName().replace(".mp3", "")
            return songPosition

    def rowCount(self, index):
        return self.playlist.mediaCount()

class SecondWindow(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.startBtn.clicked.connect(self.startDownload)
        self.download_folderBtn.clicked.connect(self.openDownloadFolder)

    def mostra(self):
        self.show()

    def openDownloadFolder(self):
        downloadFolderName = QFileDialog.getExistingDirectory(
            self, "open folder", "c:\\")
        self.download_folder.setText(downloadFolderName)
        # return downloadFolderName e.g.("E:/Download")

    def startDownload(self):  # def startDownload(self, YTlink, download_folder)#TODO
        YTlink = self.youtube_link.text()
        # download_folder = "E:/Download"

        if self.download_folder.text() != "":
            download_folder = self.download_folder.text()
        else:
            try:
                download_folder = yaml_loader()['default_folder']
                os.makedirs(download_folder)
            except:
                print("già esiste")
        # array with conversion options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': download_folder+'/%(title)s.%(ext)s',

        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([YTlink])

            # gettin id and title of song(don't need)
            # info_dict = ydl.extract_info(YTlink)
            # video_id = info_dict.get("id", None)
            # video_title = info_dict.get('title', None)

class Window(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.data = yaml_loader()

        self.setupUi(self)

        self.xCor = self.data['last_position']['xPos']
        self.yCor = self.data['last_position']['yPos']
        self.widthSize = self.data['last_window_size']['width']
        self.heightSize = self.data['last_window_size']['heigth']

        # self.resize(self.MainData['last_window_size']['width'], self.MainData['last_window_size']['heigth'])
        # self.setGeometry(self.MainData['last_position']['xPos'], self.MainData['last_position']['yPos'],self.MainData['last_window_size']['width'], self.MainData['last_window_size']['heigth'])
        self.setGeometry(self.xCor, self.yCor, self.widthSize,
                         self.heightSize)

        self.setWindowTitle("ti sputo fy")

        self.secondWindow = SecondWindow()
        # create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # open button
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionOpen_Folder.triggered.connect(self.open_folder)

        # download button
        self.actionOpenSecondWindow.triggered.connect(self.openSecondWindow)

        # play button
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # playlist button
        self.nextBtn.clicked.connect(self.next)
        self.nextBtn.setIcon(self.style().standardIcon(
            QStyle.SP_MediaSeekForward))

        self.prevBtn.clicked.connect(self.previous)
        self.prevBtn.setIcon(self.style().standardIcon(
            QStyle.SP_MediaSeekBackward))

        self.shuffleBtn.clicked.connect(self.shuffle)  # TODO icon
        self.loopBtn.clicked.connect(self.loop)  # TODO icon

        # duration slider
        self.durationSlider.sliderMoved.connect(self.set_position)

        # volumeSlider
        self.volumeSlider.setProperty("value", 100)

        # volumeBtn
        self.volumeBtn.setIcon(
            self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volumeBtn.clicked.connect(self.volumeToggle)
        self.i_volume = 0

        # clear the playlist
        self.playlistIsEmpty = True

        # media player signals

        self.mediaPlayer.stateChanged.connect(
            self.mediastate_changed)  # change play/pause btn icon
        self.mediaPlayer.positionChanged.connect(
            self.position_changed)  # duration slider avanza
        self.mediaPlayer.durationChanged.connect(
            self.duration_changed)  # set range of duration slider
        self.mediaPlayer.durationChanged.connect(self.printa)  # TODO
        # set Volume with the value from volume slider
        self.volumeSlider.valueChanged.connect(self.setVolume)

        self.mediaPlayer.positionChanged.connect(
            self.update_time_remaining)  # time remaining label
        # se muovi lo slider il video va avanti
        self.durationSlider.valueChanged.connect(self.mediaPlayer.setPosition)

        # appena finisce la canzone va avanti di una traccia e la playa
        self.mediaPlayer.mediaStatusChanged.connect(self.autoNextTrack)

        # appena finisce la canzone ed è in playbackmode 3 play la successiva
        self.mediaPlayer.mediaStatusChanged.connect(self.loopMode)

        # appena finisce la canzone ed è in playbackmode 4 playa una canzone random
        self.mediaPlayer.mediaStatusChanged.connect(self.shuffleMode)

        # create the playlist
        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(2)
        self.mediaPlayer.setPlaylist(self.playlist)

        self.playlist.currentIndexChanged.connect(self.setTitle)

        # non so perché ma va model
        self.model = PlaylistModel(self.playlist)
        self.playlistView.setModel(self.model)
        self.playlist.currentIndexChanged.connect(
            self.playlist_position_changed)
        selection_model = self.playlistView.selectionModel()
        selection_model.selectionChanged.connect(
            self.playlist_selection_changed)

        # app.aboutToQuit.connect(self.moveEvent)

    def setTitle(self):
        self.setWindowTitle(
            f"ti sputo fy - {self.playlist.currentMedia().canonicalUrl().fileName()} - {self.playlist.currentIndex()+1}/{self.playlist.mediaCount()}")

    def closeEvent(self, event):
        # retrieve position
        xAxis = self.pos().x()
        yAxis = self.pos().y()
        
        self.data['last_position']['xPos'] = xAxis
        self.data['last_position']['yPos'] = yAxis
        
        # retrieve size
        width = self.width()
        height = self.height()
        
        self.data['last_window_size']['width'] = width
        self.data['last_window_size']['heigth'] = height
        
        yaml_dump(self.data)

    
    
    
    
    
    # def moveEvent(self, event):    # QMoveEvent
    #     xAxis = event.pos().x()
    #     yAxis = event.pos().y()
    #     self.data['last_position']['xPos'] = xAxis
    #     self.data['last_position']['yPos'] = yAxis
    #     yaml_dump(self.data)

        # super(Window, self).moveEvent(event)

    # def resizeEvent(self, event):
    #     width = self.width()
    #     height = self.height()
    #     # print(width, height)
    #     self.data['last_window_size']['width'] = width
    #     self.data['last_window_size']['heigth'] = height
    #     yaml_dump(self.data)
    #     super().resizeEvent(event)

    def playlist_position_changed(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.playlistView.setCurrentIndex(ix)

    def playlist_selection_changed(self, ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        self.playlist.setCurrentIndex(i)

    def autoNextTrack(self):
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.EndOfMedia:
            # index starts from 0       mediacount starts from 1
            if self.playlist.currentIndex() != self.playlist.mediaCount()-1:
                self.playlist.next()
                self.mediaPlayer.play()

    def loopMode(self):
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.EndOfMedia:
            if self.playlist.playbackMode() == 3:
                self.playlist.next()
                self.mediaPlayer.play()

    def shuffleMode(self):
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.EndOfMedia:
            if self.playlist.playbackMode() == 4:
                while self.playlist.previousIndex() == self.playlist.currentIndex():
                    self.playlist.setCurrentIndex(
                        random.randint(0, self.playlist.mediaCount()-1))

                # ti serve sapere che è l'ultima canzone così puoi farlo ripartire
                if self.playlist.currentIndex() == self.playlist.mediaCount()-1:
                    while self.playlist.currentIndex() == self.playlist.mediaCount()-1:
                        self.playlist.setCurrentIndex(
                            random.randint(0, self.playlist.mediaCount()-1))
                self.mediaPlayer.play()

        # self.playlist.currentMediaChanged.connect(self.songChanged)

    def songChanged(self, media):
        if not media.isNull():
            url = media.canonicalUrl()
        print((url.fileName()))
        # print((MP3(f"{foldername}/{url.fileName()}")).info.length)
        songLength = round(
            (MP3(f"E:/Download/canzoni_test2/{url.fileName()}")).info.length, 0)
        print(f"{songLength} songLegth")
        tempo = str(datetime.timedelta(seconds=songLength))
        self.total_timeLabel.setText(str(tempo))  # TODO

    def next(self):
        self.playlist.next()

    def previous(self):
        self.playlist.previous()

    def shuffle(self):
        self.playlist.setPlaybackMode(4)

    def loop(self):
        self.playlist.setPlaybackMode(3)

    # TODO
    def printa(self, duration):
        print(f"{duration} duration")

    def openSecondWindow(self):
        self.secondWindow.mostra()

    def open_folder(self):
        foldername = QFileDialog.getExistingDirectory(
            self, "open folder", "c:\\")

        if foldername != '':
            self.playlist.clear()
            for song in os.listdir(foldername):
                self.playlist.addMedia(QMediaContent(
                    QUrl(f"{foldername}/{song}")))
                # self.textBrowser.append(song.replace(".mp3", ""))
            self.playlist.setCurrentIndex(0)
            self.playBtn.setEnabled(True)
            self.playlistIsEmpty = False
            self.model.layoutChanged.emit()
            self.setTitle()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            if self.playlistIsEmpty == False:
                self.playlist.clear()
                self.playlistIsEmpty = True
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            self.model.layoutChanged.emit()
            self.setTitle()

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.durationSlider.setValue(position)

    def duration_changed(self, duration):
        self.durationSlider.setRange(0, duration)
        self.total_timeLabel.setText(
            str(datetime.timedelta(seconds=round(duration/1000))))

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def update_time_remaining(self, position):
        if position >= 0:
            print(position/1000)  # TODO
            self.time_remainingLabel.setText(str(position/1000))

        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        self.durationSlider.blockSignals(True)
        self.durationSlider.setValue(position)
        self.durationSlider.blockSignals(False)

    def volumeToggle(self):
        if self.i_volume == 0:
            self.mediaPlayer.setVolume(0)
            self.volumeBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
            self.i_volume = 1
        elif self.i_volume == 1:
            if self.volumeSlider.value() == 0:
                self.volumeSlider.setValue(10)
                self.volumeBtn.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaVolume))
            else:
                self.mediaPlayer.setVolume(self.volumeSlider.value())
                self.volumeBtn.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaVolume))
            self.i_volume = 0

    def setVolume(self):
        self.mediaPlayer.setVolume(self.volumeSlider.value())
        if self.volumeSlider.value() == 0:
            self.i_volume = 0
            self.volumeToggle()
        else:
            self.i_volume = 0
            self.volumeBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaVolume))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    window = Window()
    window.show()
    config(window.height(), window.width())  # TODO

    sys.exit(app.exec_())
