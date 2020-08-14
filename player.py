
from __future__ import unicode_literals

import datetime  # in teoria l'ho rimosso creando la funzione time_format()#TODO
import os
import random
import sys

import yaml
import youtube_dl
from mutagen.mp3 import MP3
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QAbstractListModel, Qt, QTimer, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimedia import (QMediaContent, QMediaPlayer,
                                QMediaPlayerControl, QMediaPlaylist)
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout, QLineEdit, QMainWindow,
                             QPushButton, QStyle, QVBoxLayout, QShortcut)

from SecondWindow import Ui_Dialog
from sputofy import Ui_MainWindow


def time_format(seconds): # format seconds into hh:mm:ss
    mm, ss = divmod(seconds, 60)
    hh, mm = divmod(mm, 60)
    if seconds >= 3600:
        s = "%d:%02d:%02d" % (hh, mm, ss)
    else:
        s = "%d:%02d" % (mm, ss)
    
    return s

def yaml_loader(): # load config
    with open("audioPlayer/config.yaml", "r") as config:
        data = yaml.load(config, Loader=yaml.FullLoader)
        return data

def yaml_dump(data): # rewrite config
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
        self.data['last_window_size']['width'] = self.width
        self.data['last_window_size']['heigth'] = self.height
        yaml_dump(self.data)  # TODO è gia nella main window

class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            song = media.canonicalUrl().fileName().replace(".mp3","")
            songPosition = f"#{index.row()+1}    {song}"
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

    def startDownload(self):  
        YTlink = self.youtube_link.text()

        if self.download_folder.text() != "":
            download_folder = self.download_folder.text()
        else:
            try:
                download_folder = yaml_loader()['default_folder']
                os.makedirs(download_folder)
            except:
                download_folder = yaml_loader()['default_folder']
                print(f"folder already existing : {download_folder}")#TODO da testare
        
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
            try:
                ydl.download([YTlink])
            except:
                print("insert a valid url")

            # gettin id and title of song(don't need)
            # info_dict = ydl.extract_info(YTlink)
            # video_id = info_dict.get("id", None)
            # video_title = info_dict.get('title', None)

class Window(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # load config
        self.data = yaml_loader()

        # load ui
        self.setupUi(self)
        
        self.setWindowTitle("ti sputo fy")

        # "libary"
        self.xCor = self.data['last_position']['xPos']
        self.yCor = self.data['last_position']['yPos']
        self.widthSize = self.data['last_window_size']['width']
        self.heightSize = self.data['last_window_size']['heigth']

        self.setGeometry(self.xCor, self.yCor, self.widthSize,self.heightSize)
        
        #load secondWindow
        self.secondWindow = SecondWindow()

        
        
        
        # open secondWindow using button
        self.actionOpenSecondWindow.triggered.connect(self.secondWindow.mostra)

        #===========================  mediaplayer  ==============================
        
        # create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        
        # open button
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionOpen_Folder.triggered.connect(self.open_folder)

        

        # play button
        self.playBtn.setEnabled(False)
        self.playBtn.clicked.connect(self.play_video)# when btn is pressed: if it is playing it pause and change icon, if it is paused it play and change icon
        QShortcut('Space', self, lambda:self.play_video())
        # QShortcut(QKeySequence("Space"), self).activated.connect(self.play_video)metodo da ricordare in caso di problemi #TODO

        
        
        

        
        
        # duration slider
        self.durationSlider.setEnabled(False)
        self.durationSliderMaxValue = 0
        self.durationSlider.valueChanged.connect(self.mediaPlayer.setPosition)# set mediaPlayer position using the value took from the slider
        QShortcut('Right', self, lambda:self.durationSlider.setValue(self.durationSlider.value()+10000))# 1s = 1000ms
        QShortcut('Left', self, lambda:self.durationSlider.setValue(self.durationSlider.value()-10000))# 1s = 1000ms


        QShortcut('Shift+Right', self, lambda:self.durationSlider.setValue(self.durationSliderMaxValue-1000))
        QShortcut('Shift+Left', self, lambda:self.durationSlider.setValue(0))

        
        # volumeSlider
        self.volumeSlider.setProperty("value", 100)
        self.volumeSlider.valueChanged.connect(self.setVolume)# set mediaPlayer volume using the value took from the slider
        QShortcut('Up', self, lambda:self.volumeSlider.setValue(self.volumeSlider.value()+1))
        QShortcut('Down', self, lambda:self.volumeSlider.setValue(self.volumeSlider.value()-1))

        QShortcut('Shift+Up', self, lambda:self.volumeSlider.setValue(100))
        QShortcut('Shift+Down', self, lambda:self.volumeSlider.setValue(0))


        

        # volumeBtn
        self.volumeBtn.clicked.connect(self.volumeToggle)# change btn icon using mediaPlayer volume and volume slider movements
        self.i_volume = 0



        # media player signals
        self.mediaPlayer.durationChanged.connect(self.duration_changed)  # set range of duration slider
        self.mediaPlayer.positionChanged.connect(self.position_changed)  # duration slider progress
        self.mediaPlayer.stateChanged.connect(self.player_state)# see when it's playing or in pause 
        
        #===========================  playlist  ==============================
        
        # create the playlist
        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(2)
        self.mediaPlayer.setPlaylist(self.playlist)

        # clear the playlist
        self.playlistIsEmpty = True

        # non so perché ma va model
        self.model = PlaylistModel(self.playlist)
        self.playlistView.setModel(self.model)
        self.playlist.currentIndexChanged.connect(self.playlist_position_changed)
        selection_model = self.playlistView.selectionModel()
        selection_model.selectionChanged.connect(self.playlist_selection_changed)
        
        
        #===========================  playlist function  ==============================
        
        # add song name on title
        self.playlist.currentIndexChanged.connect(self.setTitle)
        
        
        # playlist button
        self.nextBtn.clicked.connect(self.playlist.next)# seek track forward
        QShortcut('D', self, lambda:self.playlist.next())

        self.prevBtn.clicked.connect(self.playlist.previous)# seek track backward
        QShortcut('A', self, lambda:self.playlist.previous())        

        
        self.mediaPlayer.mediaStatusChanged.connect(self.autoNextTrack)# once song is ended seek track forward and play it
                                                                         

        self.actionLoopIt.triggered.connect(self.loopSong)# (1) loop the same song
        
        self.loopBtn.clicked.connect(self.loop)# (3) loop the playlist  
        QShortcut('L', self, lambda:self.loop())
        
        self.randomBtn.clicked.connect(self.random)# (4) play random song without end
        QShortcut('R', self, lambda:self.random())
        
        
    

    
    def open_folder(self):
        foldername = QFileDialog.getExistingDirectory(self, "Open folder", "c:\\")

        if foldername != '':
            self.playlist.clear()
            for song in os.listdir(foldername):
                self.playlist.addMedia(QMediaContent(QUrl(f"{foldername}/{song}")))
            
            self.playlist.setCurrentIndex(0)

            self.playBtn.setEnabled(True)
            self.durationSlider.setEnabled(True)
            self.playlistIsEmpty = False

            self.model.layoutChanged.emit()
            self.setTitle()

            # adjust play/pause icon
            self.mediaPlayer.pause()
           

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Song", "c:\\")

        if filename != '':
            if self.playlistIsEmpty == False:
                self.playlist.clear()
                self.playlistIsEmpty = True
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(filename)))

            self.playBtn.setEnabled(True)
            self.durationSlider.setEnabled(True)

            self.model.layoutChanged.emit()
            self.setTitle()
            
            # adjust play/pause icon
            if self.playlist.mediaCount() == 1:
                self.playlist.setCurrentIndex(0)
                self.mediaPlayer.pause()
            
            
           

    def setTitle(self):
        self.setWindowTitle(f"ti sputo fy - {self.playlist.currentMedia().canonicalUrl().fileName()} - {self.playlist.currentIndex()+1}/{self.playlist.mediaCount()}")

    def play_video(self):
        if not self.durationSlider.isEnabled() == False: 
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.pause()
            
            else:
                self.mediaPlayer.play()

    def duration_changed(self, duration):
        self.durationSlider.setRange(0, duration)
        if duration >= 0:
            self.total_timeLabel.setText(time_format(round(duration/1000)))
        self.durationSliderMaxValue = duration

    def position_changed(self, position):
        if position >= 0:
            self.time_remainingLabel.setText(time_format((position/1000)))
        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        
        self.durationSlider.blockSignals(True)
        self.durationSlider.setValue(position)
        self.durationSlider.blockSignals(False)

    def playlist_position_changed(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.playlistView.setCurrentIndex(ix)

    def playlist_selection_changed(self, ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        self.playlist.setCurrentIndex(i)
    
#================== Playback Settings ==================#    
    
    def loopSong(self):
        if self.playlist.playbackMode() != 1:

            self.playlist.setPlaybackMode(1)

            self.actionLoopIt.setText("Loop it: ON")
            self.loopBtn.setIcon(QIcon("audioPlayer/res/loopIconOFF.svg"))
            self.randomBtn.setIcon(QIcon("audioPlayer/res/randomIconOFF.svg"))
        else:
            self.playlist.setPlaybackMode(2)
            self.actionLoopIt.setText("Loop it: OFF")
    
    def loop(self):
        if self.playlist.playbackMode() != 3:
            self.playlist.setPlaybackMode(3)

            self.loopBtn.setIcon(QIcon("audioPlayer/res/loopIconON.svg"))
            self.randomBtn.setIcon(QIcon("audioPlayer/res/randomIconOFF.svg"))
            self.actionLoopIt.setText("Loop it: OFF")

        else:
            self.playlist.setPlaybackMode(2)
            self.loopBtn.setIcon(QIcon("audioPlayer/res/loopIconOFF.svg"))
            
    def random(self):
        if self.playlist.playbackMode() != 4:
            self.playlist.setPlaybackMode(4)

            self.randomBtn.setIcon(QIcon("audioPlayer/res/randomIconON.svg"))
            self.loopBtn.setIcon(QIcon("audioPlayer/res/loopIconOFF.svg"))
            self.actionLoopIt.setText("Loop it: OFF")

        else:
            self.playlist.setPlaybackMode(2)
            self.randomBtn.setIcon(QIcon("audioPlayer/res/randomIconOFF.svg"))
            
    def autoNextTrack(self):
        
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.EndOfMedia:
            if self.playlist.playbackMode() == 2:
                # index starts from 0       mediacount starts from 1
                if self.playlist.currentIndex() != self.playlist.mediaCount()-1:
                    self.playlist.next()
                    self.mediaPlayer.play()
                else:
                    self.playlist.setCurrentIndex(0)
                    self.mediaPlayer.pause()

            # loop playlist
            elif self.playlist.playbackMode() == 3:
                self.playlist.next()
                self.mediaPlayer.play()
            
            # random song
            elif self.playlist.playbackMode() == 4:
                while self.playlist.previousIndex() == self.playlist.currentIndex():
                    self.playlist.setCurrentIndex(random.randint(0, self.playlist.mediaCount()-1))

#=======================================================#               
    def volumeToggle(self):
        if self.i_volume == 0:

            self.mediaPlayer.setVolume(0)
            self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))

            self.i_volume = 1

        elif self.i_volume == 1:

            if self.volumeSlider.value() == 0:

                self.volumeSlider.setValue(10)
                self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
            
            else:

                self.mediaPlayer.setVolume(self.volumeSlider.value())
                self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
            self.i_volume = 0

    def setVolume(self):
        self.mediaPlayer.setVolume(self.volumeSlider.value())
        
        if self.volumeSlider.value() == 0:

            self.i_volume = 0
            self.volumeToggle()

        else:

            self.i_volume = 0
            self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
    
    def closeEvent(self, event): #event handler that take window information and save it in config before the window close
        # retrieve position
        xAxis = self.geometry().x()
        yAxis = self.geometry().y()
        
        self.data['last_position']['xPos'] = xAxis
        self.data['last_position']['yPos'] = yAxis
        
        # retrieve size
        width = self.width()
        height = self.height()
        
        self.data['last_window_size']['width'] = width
        self.data['last_window_size']['heigth'] = height
        
        yaml_dump(self.data)

    def player_state(self, event):
        if event == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        elif event == QMediaPlayer.PausedState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    window = Window()
    window.show()
    config(window.height(), window.width())

    sys.exit(app.exec_())

#TODO palette
#TODO save custom playlist